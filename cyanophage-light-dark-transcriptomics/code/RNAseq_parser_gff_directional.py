#!/usr/bin/env python

'''
Steve Biller, Dec 2010 - Oct 2011, Feb 2012

Usage: RNAseq_parser_gff.py -i <input SAM-formatted alignment file> -o <output> -d <dir with gff files> -p <tells it to print out intergenics)
IMPORTANT: Script requires a tab-delimited file of annotated genome regions for each reference genome with reads mapped, name of <chromosome_name>.gff
->This is currently set up to use the GFF3 annotation file format

I know that this code is awful and clunky and could be better written... but at least it works for now

If mapping RNAseq reads against multiple reference genomes (ie for a phage and its host) both chromosomes should have been in one multi-fasta file for the bwa alignment reference

DEPENDENCIES:
-needs samtools installed in path
-requires pysam module

Goal: count number of transcripts hitting a defined genomic region, and figure out how many of those are sense vs antisense (given orientation expected of dUTP second strand protocol)

This script takes a SAM alignment file (generated by BWA, etc), then utilizes the samtools package to convert it into an indexed binary SAM file which is then used to count the number
of reads aligning to a given region using the fetch() method from pysam

Still need to fix:  
-should probably update old-style OptionParser references to use the newer argparse calls... but this works fine for now - esp if Python is not V 2.7

NOTES ABOUT COUNTING APPROACH:
If a read (paired or unpaired) spans two ORFs, then it will be counted once in each ORF

For paired end reads.... if both ends map within one ORF region, then that fragment is only counted once.  If one end is in one ORF and the other end is at least partially in another ORF, then it counts once in each.

'''

import sys, re, pysam, os
from optparse import OptionParser
from operator import itemgetter

#Define columns in genome file where relevant information are located (first column=0)
strand_column = 6 #Strand, + or -
begin_column = 3 #Gene start
end_column = 4 #Gene end
type_column = 2
info_column = 8

feature_types=["CDS","rRNA","tRNA"]

dirname="./"

printIntergics=False
printedHeader=False

#tag to indicate header line to ignore in genome file
headertag="#"

#initialize stuff
reads_in_region = {}
sense_in_region = {}
antisense_in_region = {}

allregionlists={}
alllengthlists={}

totalreads = 0
totalreads_rna = 0

def check_files(samname,reference_length_list):
    #This function verifies that all genome table files are present, and that the binary indexed BAM files exist (or will generate them if needed)
    #Returns the name of the sorted bam file to be used for read counting

    #check genome table files
    for item in reference_length_list:
        chromosome_name=item[0]
        genome_file_name=dirname+"/"+chromosome_name+".gff"
 #       print "looking for "+genome_file_name
        if not os.path.isfile(genome_file_name):
            err_msg= "Missing genome table file for chromosome %s, should be named %s" % (chromosome_name,genome_file_name)
            sys.exit(err_msg)
    
    #To do this searching efficiently, we need to use a sorted, indexed file in BAM format... check if it's there already, if not, call samtools to make them
    #depends on this naming scheme: for file 'aln', would be aln.sam -> aln.bam -> aln-sorted.bam
    
    basename = samname[0:-4]
    bamname = basename+".bam"
    if not os.path.isfile(bamname):
        print "Converting SAM file to BAM format"
        callstring = "samtools view -bS -o %s %s" % (bamname,samname)
        os.system(callstring)
                  
    sortedname = basename+"-sorted.bam"
                  
    if not os.path.isfile(basename+"-sorted.bam"):
        print "Sorting and indexing BAM file"
        os.system("samtools sort %s %s" % (bamname,basename+"-sorted"))
        os.system("samtools index %s" % (basename+"-sorted.bam"))

    return basename+"-sorted.bam"

def read_genome_table(chromosome_name):
    #Read in ORF/feature defintions from a tab-delimited file; assume that name must be <chromosome_name>.txt
    #Returns two lists, one of all orfs, one of the intergenic regions in this genome
    
    filename=dirname+"/"+chromosome_name+".gff"
    file_handle=open(filename,"rU")

    allorfs=list()
    for line in file_handle:
        #skip a header line
        if (line.strip()=='##FASTA'):
            break
        elif (line[0]==headertag):
            continue
        else:
            #print line
            parts = line.split("\t")

            if parts[type_column] in feature_types:

                infostr=parts[info_column].strip()
                infoparts = infostr.split(";")
                nameindex=0
                index=0
                for item in infoparts:
                    if "Name=" in item:
                        nameindex=index             
                    index+=1

                orfinfo = (infoparts[0],parts[strand_column],int(parts[begin_column]),int(parts[end_column]),infoparts[nameindex].strip())
                allorfs.append(orfinfo)

    #Make sure that the ORFs are in linear order, helps with defining intergenic regions in the next step
    #Intergenic regions are treated differently for RPKMO calculation
    allorfs = sorted(allorfs, key=itemgetter(2))

    intergenic_regions=list()

    #define intergenic regions and make a list of them 
    last_end = 0
    final_end = 0

    #Iterate through the defined ORF regions and generate locations between these
    for item in allorfs:
        start=item[2]
        end=item[3]
        if(start-last_end > 1):
            #intergenic region exists
            thisinfo = ("intergenic_"+str(last_end+1)+"_"+str(start-1),"+",last_end+1,start-1)
            intergenic_regions.append(thisinfo)
            last_end=end
        if(end>final_end):
            final_end=end

    #check on trailing intergenic between last feature and end of reference sequence - at some point this needs to be merged with any
    #intergenic space starting at position 1 (not sure if samtools understands circular chromosomes)
    if(reference_length > final_end):
        thisinfo = ("intergenic_"+str(final_end+1)+"_"+str(reference_length),"+",final_end+1,reference_length)
        intergenic_regions.append(thisinfo)

    file_handle.close()

    return allorfs, intergenic_regions
        
def count_reads_in_region(chromosome_name,first, last):
    #Use the .fetch() method from the pysam module to get a list of all the reads mapping to a given region of a chromosome, then
    #return the length of that list to get the numerical count

    #sets are much faster than lists
    #keep track of read names used within the region... if both ends are within this region, don't double-count it
    #this resets with each region, so it does not preclude counting a mate that maps within a different operon, intentionally
    processed_reads=set()

    total=0
    plus=0
    minus=0
    
    for alignedread in samfile.fetch(chromosome_name, first, last):
        
        thisname=alignedread.qname
        
        if(thisname not in processed_reads):
            total+=1
            processed_reads.add(thisname)

            if(alignedread.is_paired):
                #if paired, treat read1 and read2 as below
   
                if(alignedread.is_read1):

                    if(alignedread.is_reverse):
                        minus+=1
                    else:
                        plus+=1

                else:

                    if(alignedread.is_reverse):
                        plus+=1
                    else:
                        minus+=1
            else:
                #unpaired read

#                if(alignedread.is_read2):
#                    print "unpaired, read2"
#               else:
#                    print "unpaired, read1"

                if(alignedread.is_reverse):
                    minus+=1
                else:
                    plus+=1
                    
  
                    
    return total,plus,minus

 
def collect_data(chromosome_name,reference_length,orflist,intergeniclist):
    #Main function for going through a list of region identifiers, counting the number of reads mapped, and outputting this to a file
    
    length={}

    global totalreads
    global totalreads_rna

    #Get total number of reads that mapped to this chromosome for RPKM calculation
    myreads,x,y = count_reads_in_region(chromosome_name,1,reference_length)
    myreads_rna = 0 #variable for counting only reads that map to rna


    for item in intergeniclist:
        #go through list of intergenics, get counts of mapped reads
        strand="+"
        start=item[2]
        end=item[3]
        length[item]=end-start+1
        total,plus,minus = count_reads_in_region(chromosome_name,start,end)
        
        reads_in_region[item]=total
        sense_in_region[item]=plus
        antisense_in_region[item]=minus
    
    for item in orflist:
        #go through list of ORFs, get counts of mapped reads, keep track of totals
        strand=item[1]
        start=item[2]
        end=item[3]
        length[item]=end-start+1
        total,plus,minus = count_reads_in_region(chromosome_name,start,end)

        reads_in_region[item]=total

        #assuming dUTP directionality... read should be from second strand
        if(strand=="-"):
#        if(strand=="+"):
            sense_in_region[item]=plus
            antisense_in_region[item]=minus
        else:
            sense_in_region[item]=minus
            antisense_in_region[item]=plus
        
        if "rna" in item[0]:
            myreads_rna += reads_in_region[item]

    #Prepare for final output - make ordered master list of all regions tested
    allregions = intergeniclist+orflist
    allregions = sorted(allregions, key=itemgetter(2))

    print "   Reads mapped to this genome = "+str(myreads)
    print "   Non-RNA reads in this genome = "+str((myreads-myreads_rna))

    totalreads += myreads
    totalreads_rna += myreads_rna

    return allregions,length


def check_sam_header(infile):
    #Go through header of SAM file and parse out the genome reference name and the length of that genome
    #Returns a list with tuples of (name,length) pairs in case multiple references are submitted
    #In SAM format, SN defines reference seq name, LN is length; this has been tested with SAM files generated by BWA only
    
    reference_length_list = list()
    samhandle=open(infile,"rU")
    
    for line in samhandle:
        if (line[0] != "@"):
            break
        elif ("@SQ" in line): #header line
            m = re.search("SN:(.+?)\s",line)
            n = re.search("LN:(\d+?)\s",line)
            name = m.group(1)
            n = int(n.group(1))
            reference_length_list.append((name,n))

    samhandle.close()
    return reference_length_list

if __name__ == "__main__":
    #Main program loop
    
    usage="Usage: RNAseq_parser.py -i <input SAM-formatted alignment file> -o <output> -d <directory containing genome definition files in gff format, named chromosomename.gff> -p <print out intergenic region data>"

    #Check that all options have been passed
    if not len(sys.argv) >= 5:
        sys.exit("Error: not all arguments specified\n"+usage)
            
    parser = OptionParser(usage)
    parser.add_option("-i",dest="infile_sam",help="input SAM-formatted alignment file")
    parser.add_option("-o",dest="outfile",help="output file name")
    parser.add_option("-d",dest="dirname",help="directory containing genome definition files",default="./")
    parser.add_option("-p",action="store_true",dest="intergenics",help="print values for intergenic regions",default=False)
    (options, args) = parser.parse_args()

    #Output
    output_handle = open(options.outfile, "w")

    dirname=options.dirname
    printIntergenics=options.intergenics

    #check header of sam file
    #get length of reference sequence for determining intergenics
    reference_length_list=check_sam_header(options.infile_sam)

    #check to see if BAM indexed files exist, otherwise make them; also verify that genome table files exist before we begin processing
    bamfilename = check_files(options.infile_sam,reference_length_list)
    
    #create samfile object for all of the read counting... global
    samfile = pysam.Samfile(bamfilename, 'rb')

    #main loop for counting reads mapping to each reference chromosome in file
    for items in reference_length_list:
        reference_length = items[1]
        chromosome_name = items[0]
        print "Counting reads mapped to reference sequence %s..." %(chromosome_name)

        #generate ranges for every ORF, intergenic region for counting
        orflist,intergeniclist = read_genome_table(chromosome_name)

        #count data
        allregion,ll = collect_data(chromosome_name,reference_length,orflist,intergeniclist)
        allregionlists[chromosome_name]=allregion
        alllengthlists[chromosome_name]=ll

    for items in reference_length_list:
        chromosome_name = items[0]
        
        #header line
        if not printedHeader:
            output_handle.write("Chromosome\tRegion\tStrand\tStartCoordinate\tEndCoordinate\tName\tTotalReadsInRegion\tSenseReads\tAntisenseReads\n")
            printedHeader=True

        match = re.compile("intergenic")

        allregions=allregionlists[chromosome_name]
        length=alllengthlists[chromosome_name]

        #calculate values, write output for each defined region
        for item in allregions:

            if match.match(item[0]):#intergenic region

                if printIntergenics:
                    output_handle.write(chromosome_name+"\t"+item[0]+"\t"+item[1]+"\t"+str(item[2])+"\t"+str(item[3])+"\t"+"\t"+str(reads_in_region[item])+"\t"+str(sense_in_region[item])+"\t"+str(antisense_in_region[item])+"\n")
            
            else:

                output_handle.write(chromosome_name+"\t"+item[0]+"\t"+item[1]+"\t"+str(item[2])+"\t"+str(item[3])+"\t"+str(item[4])+"\t"+str(reads_in_region[item])+"\t"+str(sense_in_region[item])+"\t"+str(antisense_in_region[item])+"\n")

  
    output_handle.close()
    print "\nGrand total reads mapped: "+str(totalreads)+"\nGrand total non-RNA reads mapped to ORFs: "+str(totalreads-totalreads_rna)

    print "Done"
    
