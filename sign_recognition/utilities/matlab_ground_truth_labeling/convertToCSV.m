%% converts groundTruth.mat to *.csv file

% parameters
out_file="2019-01-20-15-59-41.csv";
in_file="2019-01-20-15-59-41.mat";

image_width=640;
image_height=480;
zero_class_id=00043;

% load files
load(in_file);
fileID = fopen(out_file,'w');
fprintf(fileID,'Filename,Width,Height,Roi.X1,Roi.Y1,Roi.X2,Roi.Y2,ClassId\n');

% loop over all images / timesteps
for i=1:size(gTruth.LabelData, 1)
   has_label=false;
   
   % loop over all labels
   for j=1:size(gTruth.LabelData, 2)
       
       % found label for this picture
       if not(isempty(cell2mat(gTruth.LabelData(i,j).Variables)))
           has_label=true;
           roi=cell2mat(gTruth.LabelData(i,j).Variables);
           for k=1:size(roi,1)
               fprintf(fileID,'frame%04.0f.jpg,', i-1);
               fprintf(fileID,'%d,', image_width);
               fprintf(fileID,'%d,', image_height);
               fprintf(fileID,'%d,', round(roi(k,1)));
               fprintf(fileID,'%d,', round(roi(k,2)));
               fprintf(fileID,'%d,', round(roi(k,1)+roi(k,3)));
               fprintf(fileID,'%d,', round(roi(k,2)+roi(k,4)));
               fprintf(fileID,'%d' , str2double(cell2mat(table2array(gTruth.LabelDefinitions(j,3)))));
               fprintf(fileID,'\n');
           end
       end
       
       % no label for this picture found
       if not(has_label) && j == size(gTruth.LabelData, 2)
           fprintf(fileID,'frame%04.0f.jpg,', i-1);
           fprintf(fileID,'%d,', image_width);
           fprintf(fileID,'%d,', image_height);
           fprintf(fileID,'%d,', 0);
           fprintf(fileID,'%d,', 0);
           fprintf(fileID,'%d,', 0);
           fprintf(fileID,'%d,', 0);
           fprintf(fileID,'%d' , zero_class_id);
           fprintf(fileID,'\n');
       end
   end
    
end

fclose(fileID);
