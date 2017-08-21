   row=320;  col=240;
fin=fopen('bild18.raw','r');
I=fread(fin,row*col,'uint8=>uint8'); 
Z=reshape(I,[row,col]);
%Z=Z';
k=imshow(Z)