
#   Working method....
#   run these in the folder for the version
dh_make --indep --createorig   # indep is wrong for this project as it is only for RPI but hay!

cp $source\oscpygpio.* .
cp $source\requirments.txt .

debuild -us -uc


