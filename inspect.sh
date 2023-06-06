#!/bin/bash
set -e

mkdir -p datasets

for name in civilian-harm eyesonrussia-linkedata integrated-linked-data-for-ukraine-resil ; do
    if ! test -f datasets/$name.nt ; then
        curl -s -L https://triplydb.com/shuaiwangvu/$name/download.nt.gz --output - | zcat | sort > datasets/$name.nt
    fi
done

CH=datasets/civilian-harm.nt
ER=datasets/eyesonrussia-linkedata.nt
IL=datasets/integrated-linked-data-for-ukraine-resil.nt
SM=datasets/sources-merged.nt
LA=datasets/links.nt


cat $CH $ER | sort > $SM
comm -23 $IL $SM | sort > $LA

ch_size=$(wc -l $CH | awk '{print $1}')
er_size=$(wc -l $ER | awk '{print $1}')
ch_minus_er_size=$(comm -23 $CH $ER | wc -l | awk '{print $1}')
er_minus_ch_size=$(comm -23 $ER $CH | wc -l | awk '{print $1}')

il_size=$(wc -l $IL | awk '{print $1}')
il_minus_er_size=$(comm -23 $IL $ER | wc -l | awk '{print $1}')
il_minus_ch_size=$(comm -23 $IL $CH | wc -l | awk '{print $1}')

il_minus_la=$(comm -23 $IL $LA | wc -l | awk '{print $1}')
sm_minus_il=$(comm -23 $SM $IL | wc -l | awk '{print $1}')

sm_size=$(wc -l $SM | awk '{print $1}')


echo "number of statements in civilian-harm which are not in eyesonrussia-linkedata: "
echo $ch_minus_er_size out of $ch_size
echo "number of statements in eyesonrussia-linkedata which are not in civilian-harm: "
echo $er_minus_ch_size out of $er_size

if [[ $ch_minus_er_size == $ch_size && $er_minus_ch_size == $er_size ]] ; then
    echo "Conclusion: the two source datasets have no overlap"
else
    echo "Conclusion: the two source datasets partially overlap"
fi
echo

echo "number of statements in integrated-linked-data-for-ukraine-resil which are not in civilian-harm: "
echo $il_minus_ch_size out of $il_size

echo "number of statements in integrated-linked-data-for-ukraine-resil which are not in eyesonrussia-linkedata: "
echo $il_minus_er_size out of $il_size

echo "number of statements in civilian-harm+eyesonrussia-linkedata which don't occur in integrated-linked-data-for-ukraine-resil: "
echo $sm_minus_il out of $sm_size
