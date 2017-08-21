im=imread('1057small.jpg');
im1=im(:,:,1);
im2=im(:,:,2);
im3=im(:,:,3);

[max1,I1]=min(im1,[],1);
[max2,I2]=min(im1,[],2);