function [ O ] = Resize( pic )
%RESIZE Summary of this function goes here
%   Detailed explanation goes here

O={imresize(pic{1,1},[32 32]),imresize(pic{1,2},[32 32]),imresize(pic{1,3},[32 32]),imresize(pic{1,4},[32 32])};

end

