#!/bin/bash
# Salveaza intermediarele reelului cu pompa din Blender in dosarul comun (arhive tar sub ~90 MB).
S=/tmp/claude-0/-home-claude/4d737410-20c6-5f74-8279-6fcf9634cd35/scratchpad
D=/mnt/project-files/animatii/sursa/blender-cp4/reel
W=$D/work
set -e
cd $S/reelbl
rm -f save/ov_ovl_0*.tar
python3 pack.py $S/reelbl/ov ovl $S/reelbl/save/ov_ovl
cd $S/bl
tar cf $S/reelbl/save/bl_out_reel_01.tar out_reel/C_HOT_plate.png out_reel/C_ROT0_R1 out_reel/C_ROT1_R1
tar cf $S/reelbl/save/bl_out_reel_02.tar out_reel/C_CROSS_R1 out_reel/C_HOT_R1 out_reel/C_HOT_R2
tar cf $S/reelbl/save/bl_out_reel_03.tar out_reel/W_FUEL_plate.png out_reel/W_AIR_plate.png out_reel/W_HOT_plate.png out_reel/W_FUEL_R1 out_reel/W_AIR_R1 out_reel/W_HOT_R1 out_reel/W_HOT_R2 out_reel/boxes_W.json out_reel/boxes_C.json out_reel/qA1.log out_reel/qA2.log
ls -la $S/reelbl/save/
mkdir -p $W/
for f in $S/reelbl/save/*.tar; do cp "$f" $W/ && echo "copiat $(basename $f) $(date -u +%H:%M:%S)"; done
# uneltele, la zi
cd $S/reelbl
cp README.md director.py director.json compose.py wm.py wm_pattern.py wmapply.py mask_list.py mask2_list.json motion_score.json assemble.sh finish_bl.sh render_seg.py chrome_batch.sh qa_sheet.py endgame.sh endgame_wait.sh pack.py save_work.sh $D/
cp $S/bl/reel_scene.py $S/bl/qA1.sh $S/bl/qA2.sh $S/bl/out_reel/boxes_W.json $S/bl/out_reel/boxes_C.json $D/
mkdir -p $D/anim/ $D/wm/
cp $S/anim/ovrender.cjs $S/anim/amask.cjs $S/anim/patch_reel.py $S/anim/rlib.cjs $D/anim/
cp $S/reelbl/wm/pattern.png $S/reelbl/wm/pattern.json $D/wm/
echo "SAVE_OK $(date -u +%H:%M:%S)"
