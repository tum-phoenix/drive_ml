function [ O] = ResizeSingle( pic,n )
%RESIZE Summary of this function goes here
%   Detailed explanation goes here

O=imresize(pic,[n, n]);

end

