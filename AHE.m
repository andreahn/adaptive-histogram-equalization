%
% Adaptive Histogram Equalization
% Implemented without using MatLab-provided CDF or histogram eq. functions
%

% import image 
image = imread('view.tif'); 

% histogram equalization will be done divided into (X_block * Y_block)s
X_block = 10;
Y_block = 10;

dimX = size(image,1);
dimY = size(image,2);
result = uint8(zeros(dimX,dimY));

% size of one tile and half a tile
tileX = ceil (dimX / X_block);
tileY = ceil(dimY / Y_block);
halfTileX = ceil(tileX /2);
halfTileY = ceil(tileY /2);

% will contain local CDFs for each tile
tileCDF = zeros(X_block, Y_block, 256, 256);

% compute CDF for each tile
for i=1:X_block
    for j=1:Y_block
        startX = 1 + (i - 1) * tileX;
        startY = 1 + (j - 1) * tileY;
        
        % determine tile
        if (i == X_block) && (j == Y_block)
            tile = image(startX:end, startY:end);
        elseif i == X_block
            tile = image(startX:end, startY:startY + tileY);
        elseif j == Y_block
            tile = image(startX:startX + tileX, startY:end);
        else
            tile = image(startX:startX + tileX, startY:startY + tileY);
        end
        
        tileCDF(i,j,:,:) = CDF(tile);
    end
end


for x=1:dimX
    for y=1:dimY
        
        % find tile(i,j) pixel(x,y) is located in
        i = min (floor(x / tileX) + 1, X_block);
        j = min (floor(y / tileY) + 1, Y_block);
        
        % x1 and y1 are center of tile(i,j)
        x1 = i * tileX - halfTileX;
        y1 = j * tileY - halfTileY;
        
        if (i ~= 1) &&( (i == X_block) || (x < x1))
            k = i - 1;
            x2 = x1 - tileX;
        else
            k = i + 1;
            x2 = x1 + tileX;
        end
        
        
        if (j ~= 1) &&((j == Y_block) || (y < y1))
            l = j - 1;
            y2 = y1 - tileY;
        else
            l = j + 1;
            y2 = y1 + tileY;
        end
        
        % interpolate and calculate intensity for pixel (x,y)
        
        alpha = tileCDF(i,j, image(x,y) + 1);
        beta = tileCDF(i,l, image(x,y) + 1);
        temp1 = lin_interpol (y1,y2,y, alpha, beta);
        
        alpha = tileCDF(k,j, image(x,y) + 1);
        beta = tileCDF(k,l, image(x,y) + 1);
        temp2 = lin_interpol (y1,y2,y, alpha, beta);
        
        result(x,y) = lin_interpol (x1,x2,x, temp1, temp2);
        
    end
end


% Show original and resulting image
figure, imshow(image);
title ('Original image');

figure, imshow(result);
title ('Image after Adaptive Histogram Equalization');



function result = CDF(image)

dimX = size(image,1);
dimY = size(image,2);

result = uint8(zeros(256));
p = zeros(256);
temp = zeros(256);

for i=1:dimX
    for j=1:dimY
           intensity = image(i,j) + 1;
           p(intensity) = p(intensity) + 1 / (dimX * dimY);
    end
end

% scale to intensity values
for i=1:256
    for j=1:i
        temp(i) = temp(i) + p(j);
    end
    result(i) = temp(i) * 255;
end

end

function f = lin_interpol (x1,x2,x, alpha, beta)
        w1 = abs(x1 - x);
        w2 = abs(x2 - x);
        f = round((w2 * alpha) / (w1 + w2) + (w1 * beta) / (w1 + w2));
    end