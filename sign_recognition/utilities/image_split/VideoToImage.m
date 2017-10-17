%shuttleVideo = VideoReader('signs.mp4');
% workingDir = tempname;
% mkdir(workingDir)
% mkdir(workingDir,'images')
% ii = 1;
% 
% while hasFrame(shuttleVideo)
%    img = readFrame(shuttleVideo);
%    
%    filename = [sprintf('%03d',ii) '.jpg'];
%    fullname = fullfile(workingDir,'images',filename);
%    imwrite(img,fullname)    % Write out to a JPEG file (img1.jpg, img2.jpg, etc.)
%    ii = ii+1;
% end
vidObj=VideoReader('signs002.mp4');
vidObj.CurrentTime=0.5;
frame = readFrame(vidObj);
%dest=pwd;
dest='Y:\Zero_Class_color\00043';
counter=0;
for i = 1:470
    vidObj.CurrentTime=0.5*(i-1);
    frame = readFrame(vidObj);
    frames = CutPic(frame,4);
    for j=1:size(frames,2)
       frames{j}
       baseFileName = sprintf('%05d.ppm', counter); % Name without path in front of it.
       fullFileName = fullfile(dest, baseFileName); % Prepend current folder
       imwrite(ResizeSingle(frames{j},64), fullFileName);
       counter=counter+1;
       %im(i)=image(frames);
    end
end