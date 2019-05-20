if [ -s /data/isaure/Scripts/$1 ]; then
  mv /data/isaure/Scripts/$1 /data/isaure/Scripts/OLD/$1
  rm $1
else
  mv $1 /data/isaure/Scripts/OLD/
fi
