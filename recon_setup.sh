#!/bin/bash

Tools_dir='/root/Tools'

mkdir -p $Tools_dir

echo "=======This is to setup all the tools required for recon ======"

sudo apt-get update

echo "You have following options --
	-- 1 - Amass
	-- 2 - MassDns
	-- 3 - Masscan
	-- 4 - EyeWitness
	-- 5 - SecList and filter-resolved
	-- 6 - GoBuster
	-- all - Run all of them
	-- leave - Leave the Setup"

while :
do
    read -p 'Choose option: ' input_str
    case $input_str in
	    1 | all)
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    echo "+                            Amass                                  +"
		    echo "+      https://github.com/OWASP/Amass/blob/master/doc/install.md    +"
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    sudo apt install -y snapd
		    sudo snap install amass
		    sudo systemctl start snapd
		    sudo systemctl enable snapd
		    sudo systemctl start apparmor
		    sudo systemctl enable apparmor
		    echo "AMASS_PATH=/snap/bin" >> ~/.bashrc
		    sleep 5
		    ;;&

	    2 | all)
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    echo "+                            MassDNS                                +"
		    echo "+     https://github.com/blechschmidt/massdns                       +"
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

		    git clone https://github.com/blechschmidt/massdns.git "$Tools_dir/massdns"
		    cd $Tools_dir/massdns && make
		    echo 'alias massdns="/root/Tools/massdns/bin/massdns"' >> ~/.bashrc
		    ;;&

	    3 | all)
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    echo "+                            Masscan                                +"
		    echo "+    https://github.com/robertdavidgraham/masscan                   +"
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

		    sudo apt-get install -y git gcc make libpcap-dev
		    git clone https://github.com/robertdavidgraham/masscan "$Tools_dir/masscan"
		    cd $Tools_dir/masscan && make
		    cp $Tools_dir/masscan/bin/masscan /usr/local/bin
		    ;;&

	    4 | all)
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    echo "+                         EyeWitness                                +"
		    echo "+      https://github.com/FortyNorthSecurity/EyeWitness             +"
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    git clone https://github.com/FortyNorthSecurity/EyeWitness.git "$Tools_dir/EyeWitness"
		    cd $Tools_dir/EyeWitness/setup
		    ./setup.sh
		    echo 'alias eyewitness="/root/Tools/EyeWitness/EyeWitness.py"' >> ~/.bashrc
		    ;;&

	    5 | all)
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    echo "+              SecLists and filter-resolved                         +"
		    echo "+        https://github.com/danielmiessler/SecLists                 +"
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

		    git clone https://github.com/danielmiessler/SecLists.git "$Tools_dir/SecLists"
		    snap install go --classic
		    go get github.com/tomnomnom/hacks/filter-resolved
		    echo "F_PATH=/root/go/bin" >> ~/.bashrc
		    ;;&
	    6 | all)
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    echo "+                          GoBuster                                 +"
		    echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		    go get github.com/OJ/gobuster
		    ;;

	    leave)
		    echo "export PATH=$PATH:$AMASS_PATH:$F_PATH" >> ~/.bashrc
		    source ~/.bashrc
		    exit
		    ;;

	    *)
		    echo "Enter a valid option"
		    ;;
	esac
done
