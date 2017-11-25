%% converts groundTruth.mat to *.csv file

% parameters
out_file="~/Downloads/mount/GT-00000.csv";
in_file="~/Downloads/mount/labels.mat";

image_width=640;
image_height=480;
zero_class_id=00043;

% load files
load(in_file);
fileID = fopen(out_file,'w');
fprintf(fileID,'Filename;Width;Height;Roi.X1;Roi.Y1;Roi.X2;Roi.Y2;ClassId\n');

% loop over all images / timesteps
for i=1:size(gTruth.LabelData, 1)
   has_label=false;
   
   % loop over all labels
   for j=1:size(gTruth.LabelData, 2)
       
       % found label for this picture
       if not(isempty(cell2mat(gTruth.LabelData(i,j).Variables)))
           has_label=true;
           roi=cell2mat(gTruth.LabelData(i,j).Variables);
           fprintf(fileID,'%05.0f.png;', i);
           fprintf(fileID,'%d;', image_width);
           fprintf(fileID,'%d;', image_height);
           fprintf(fileID,'%d;', round(roi(1)));
           fprintf(fileID,'%d;', round(roi(2)));
           fprintf(fileID,'%d;', round(roi(1)+roi(3)));
           fprintf(fileID,'%d;', round(roi(2)+roi(4)));
           fprintf(fileID,'%d' , str2double(cell2mat(table2array(gTruth.LabelDefinitions(j,3)))));
           fprintf(fileID,'\n');
       end
       
       % no label for this picture found
       if not(has_label) && j == size(gTruth.LabelData, 2)
           fprintf(fileID,'%05.0f.png;', i);
           fprintf(fileID,'%d;', image_width);
           fprintf(fileID,'%d;', image_height);
           fprintf(fileID,'%d;', 0);
           fprintf(fileID,'%d;', 0);
           fprintf(fileID,'%d;', 0);
           fprintf(fileID,'%d;', 0);
           fprintf(fileID,'%d' , zero_class_id);
           fprintf(fileID,'\n');
       end
   end
    
end

fclose(fileID);