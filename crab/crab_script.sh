#this is not mean to be run locally
#
echo Check if TTY
if [ "`tty`" != "not a tty" ]; then
    echo "YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES"
else
    ls -lR .
    # echo "ENV..................................."
    # env
    echo "VOMS"
    voms-proxy-info -all
    echo "CMSSW BASE, python path, pwd"
    echo $CMSSW_BASE
    echo $PYTHON_PATH
    echo $PWD
    # rm -rf $CMSSW_BASE/lib/
    # rm -rf $CMSSW_BASE/src/
    # rm -rf $CMSSW_BASE/module/
    # rm -rf $CMSSW_BASE/python/
    # mv lib $CMSSW_BASE/lib
    # mv src $CMSSW_BASE/src
    # mv module $CMSSW_BASE/module
    # mv python $CMSSW_BASE/python
    echo Found Proxy in: $X509_USER_PROXY

    for i in "$@"; do
	case $i in
	    process=*)
	    opt_proc="${i#*=}"
	    ;;
	    year=*)
	    opt_year="${i#*=}"
	    ;;
	esac
    done
    echo "process: ${opt_proc} year: ${opt_year}"
    echo "---> python processors/reweight.py"
    python processors/reweight.py --crab --process "${opt_proc}"  --year "${opt_year}"
    echo "DONE with crab_script.sh"
fi
