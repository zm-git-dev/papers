% plotHumannMap.m

clear;      % clears workspace variables
clc;        % clears command window
close all;  % closes any figure windows

load_colormaps

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Environmental & original "humannAll" data
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

fid = fopen('/Users/luke/krse2011/db/krse2011_v3_humann_KOrelAbund.csv');
nCols = 5794; % wc -l list.KOrelAbund.tsv
hformat = repmat('%s', [1 nCols]);
header = textscan(fid, hformat, 1, 'delimiter', ',');
format = repmat('%f', [1 nCols]);
data = textscan(fid, format, 'delimiter', ',');
fclose(fid);

station      = data{1};
latitude     = data{2};
longitude    = data{3};
xcoord       = data{4};
ycoord       = data{5};
depth        = data{6};
temperature  = data{7};
salinity     = data{8};
oxygen       = data{9};
chlorophyll  = data{10};
turbidity    = data{11};
nitrate      = data{12};
phosphate    = data{13};
silicate     = data{14};
read         = data{15};



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 3D topographic map
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% load simple topography file (generated by redseaShrinkFile.sh)
fileName = 'RedSea2m-4244.xyz';
fid = fopen(fileName);
mapdata = textscan(fid,'%f %f %f','delimiter','\t');
fclose(fid);

longD = mapdata{1};
latD = mapdata{2};
altD = mapdata{3};

c = 1;
for j = 1:size(longD,1)
    if (mod(longD(j),0.2)==0 && mod(latD(j),0.2)==0)
        long(c) = longD(j);
        lat(c) = latD(j);
        alt(c) = altD(j);
        c = c + 1;
    end
end

nlines = size(long,2);

maxlong = -180;

for i = 1:nlines
    if long(i) > maxlong
        maxlong = long(i);
    else
        break;
    end
end
    
nlong = i-1;

nlat = nlines/nlong;

x_long = long(1:nlong);

y_lat = lat(1:nlong:nlines);

z_alt = zeros(nlat,nlong);

for j = 1:nlat
    z_alt(j,:) = alt(nlong*(j-1)+1:nlong*j);
end

% ignore depths above sea level
for k = 1:nlat
    for l = 1:nlong
        if z_alt(k,l) > 0
            z_alt(k,l) = 0;
        end
    end
end

[X_long,Y_lat] = meshgrid(x_long,y_lat);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% KO plots
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% temperature  7
% salinity     8
% oxygen       9
% chlorophyll  10
% turbidity    11
% nitrate      12
% phosphate    13
% silicate     14

% 1030	K00114
% 3975	K00123
% 5253	K00285
% 704	K00301
% 705	K00302
% 3669	K00303
% 3663	K00304
% 3664	K00305
% 4264	K00315
% 5788	K00366
% 5789	K00367
% 3977	K00437
% 3971	K00438
% 3203	K00532
% 5376	K00544
% 2753	K00577
% 2282	K00925
% 1853	K01077
% 2177	K01428
% 1402	K02000
% 1401	K02001
% 1404	K02002
% 4404	K02036
% 1729	K02040
% 5305	K02575
% 337	K02588
% 3067  K06212
% 5077	K03320
% 5073	K03325
% 5613	K03839
% 4767	K04044
% 1538  K04077
% 1535	K04078
% 3064	K06217
% 110	K07175
% 5763	K07636
% 5514	K07657
% 2232	K08688
% 4023	K08928
% 4024	K08929
% 2138	K10944
% 2137	K10946
% 2219	K11959
% 3324	K14028
% 638	K14029
% 1198	K14083

%[7:14 110 337 638 704 705 1030 1198 1401 1402 1404 1535 1538 1729 1853 2137 2138 2177 2219 2232 2282 2753 3064 3067 3203 3324 3663 3664 3669 3971 3975 3977 4023 4024 4264 4404 4767 5073 5077 5253 5305 5376 5514 5613 5763 5788 5789]

for i = [7]
    
    koNone = data{i};
    koNorm = koNone/max(koNone);
        
    figure;
%     cmap_cool = cool;
%     cmap_cyan_black = [zeros(64,1) cmap_cool(:,2) cmap_cool(:,2)];
    colormap(cbRdBu9);
%     cmap_yellow_black = flipud([cmap_autumn(:,2) cmap_autumn(:,2) cmap_autumn(:,3)]);
%     colormap(cmap_yellow_black);
    scatter3(longitude,latitude,-depth,50,koNorm,'LineWidth',2);
    
    px = xlabel('Longitude (\circ{}E)');
    py = ylabel('Latitude (\circ{}N)');
    pz = zlabel('Depth (m)');
    
    axis([32 44 12 30 -500 0]);
    %set(gca,'ZScale','log');

    set(gca,'ZTick',[-500:50:0]);
    set(gca,'ZTickLabel',{'500'; '450'; '400'; '350'; '300'; '250'; '200'; '150'; '100'; '50'; '0'});
        
    view(-30,20);
    
    ystring = header{i};
    outfile = ['map_',ystring{1},'.eps'];
    
    saveas(gcf,outfile,'epsc');
    
end

