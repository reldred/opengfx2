export PATH=$PATH:$(pwd)

cd infrastructure

cd 64
infrastructure_roadrail_terrainoverlay.py 1 rail
infrastructure_roadrail_terrainoverlay.py 1 road
infrastructure_roadrail_terrainoverlay.py 1 road_noline
infrastructure_roadrail_terrainoverlay.py 1 road_town
infrastructure_levelcrossing_infrastructureoverlay.py 1
infrastructure_canalriver_terrainoverlay.py 1 canal
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 128
infrastructure_roadrail_terrainoverlay.py 2 rail
infrastructure_roadrail_terrainoverlay.py 2 road
infrastructure_roadrail_terrainoverlay.py 2 road_noline
infrastructure_roadrail_terrainoverlay.py 2 road_town
infrastructure_levelcrossing_infrastructureoverlay.py 2
infrastructure_canalriver_terrainoverlay.py 2 canal
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd 256
infrastructure_roadrail_terrainoverlay.py 4 rail
infrastructure_roadrail_terrainoverlay.py 4 road
infrastructure_roadrail_terrainoverlay.py 4 road_noline
infrastructure_roadrail_terrainoverlay.py 4 road_town
infrastructure_levelcrossing_infrastructureoverlay.py 4
infrastructure_canalriver_terrainoverlay.py 4 canal
custom_dither.py
cd pygen
custom_dither.py
cd ../..

cd ..