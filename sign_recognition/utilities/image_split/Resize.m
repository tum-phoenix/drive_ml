function [ O ] = Resize( pic,n )
%RESIZE Summary of this function goes here
%   Detailed explanation goes here

O={imresize(pic{1,1},[n n]),imresize(pic{1,2},[n n]),imresize(pic{1,3},[n n]),imresize(pic{1,4},[n n])};

end

