A = imread('1057.jpg');
E=CutPic(A,16);

for i=1:4
   for j=1:4
       
       
       imwrite(ResizeSingle(E{i}{j},64),sprintf('Pic%d%d.jpg',i,j));
       
   end    
end