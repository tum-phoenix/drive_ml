function [ img2 ] = CutPic( img,i);
%CUTPIC Summary of this function goes here
%
    a=size(img);
    img2=img((a(1)/2):(a(1)-a(1)*0.1),:,:);
    
    if(i==4)
    img2={img((a(1)/2):(a(1)-a(1)*0.1),1:200,:),img((a(1)/2):(a(1)-a(1)*0.1),140:340,:),img((a(1)/2):(a(1)-a(1)*0.1),200:500,:),img((a(1)/2):(a(1)-a(1)*0.1),440:640,:)};    
        
    end
    
    
end

