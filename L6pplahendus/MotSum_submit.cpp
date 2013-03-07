#include <sqlite3.h>
#include <iostream>
#include <sstream>
#include <stdlib.h>

using namespace std;

string workStatus="";
static int callback(void *NotUsed, int argc, char **argv, char **azColName) {
	workStatus=argv[0];
	return 0;
}

static void show_usage() {
	cout << "Usage: MotSum_submit [OPTIONS]\n\n"
		<< "Submits the motif counting job and then waits for this job to be finished.\n\n"
		<< "Options:\n"
		<< "\t-h,--help\t\tshow this help message and exit\n"
		<< "\t-o,--output\t\tOutput table path and name (file will be overwriten) (required)\n"
		<< "\t-m,--motifList\t\tFile containing new-line separated motifs to search for (required)\n"
		<< "\t--noWait\t\tUse this flag to exit after job is submitted" << endl;
}


int main(int argc, char *argv[]) {
	
	string output="";
	string motifList="";
	bool noWait=0;
	
	//Argument parsing
	for (int h=1; h <argc; h++) {
		string tmp = argv[h];
		if (tmp=="--help" || tmp=="-h") {
			show_usage();
		}
		else if (tmp=="--output" || tmp=="-o") {
			h++;
			if (h <argc && argv[h][0]!='-') {
				char actualpath [PATH_MAX+1];
				realpath(argv[h], actualpath);
				output=actualpath;
			} else {
				cout << "Problem with parameters.\n Use \'MotSum_submit -h\' for more info" << endl;
				return 1;
			}
		}
		else if (tmp=="--motifList" || tmp=="-m") {
			h++;
			if (h <argc && argv[h][0]!='-') {
				char actualpath [PATH_MAX+1];
				realpath(argv[h], actualpath);
				motifList=actualpath;
			} else {
				cout << "Problem with parameters.\n Use \'MotSum_submit -h\' for more info" << endl;
				return 1;
			}
		}
		else if (tmp=="--noWait") {
			noWait=1;
		} else {
			cout << "Problem with parameters.\n Use \'MotSum_submit -h\' for more info" << endl;
			return 1;
		}
	}
	if (output=="" || motifList=="") {
		cout << "Problem with parameters.\n Use \'MotSum_submit -h\' for more info" << endl;
		return 1;
	}
	
	//Open database connection
	int error = 0;
	int workID = 0;
	sqlite3 *database;
	error = sqlite3_open("workListDB.sqlite", &database);
	if (error) {
		cout << "Submit: Can not open database (" << error << ")" << endl;
		return 1;
	}
	sqlite3_busy_timeout(database, 60000);
	//Insert work data
	string insertStatement;
	stringstream ins_ss;
	ins_ss << "INSERT INTO workList (status, motifFilePath, outFilePath) VALUES (\'Waiting\', \'" << motifList << "\', \'" << output << "\')";
	insertStatement = ins_ss.str();
	error = sqlite3_exec(database, insertStatement.c_str(), 0, 0, 0);
	if (error) {
		cout << "Submit: Can not insert to database (" << error << ")" << endl;
		return 1;
	}
	
	//Close database connection 
	sqlite3_close(database);
	cout << "Submit done (" << workID << ")" << endl;
	
	// Check noWait flag
	if (noWait==0) {
		
		//Build select query
		workID=sqlite3_last_insert_rowid(database);
		string statusQuery;
		stringstream sta_ss;
		sta_ss << "SELECT status FROM workList WHERE workID = " << workID;
		statusQuery = sta_ss.str();
		
		//Loop every 30s untill work finished
		while (1) {
			sleep(30);
			error = sqlite3_open("workListDB.sqlite", &database);
			if (error) {
				cout << "Check: Can not open database (" << error << ")" << endl;
				return 1;
			}
			error = sqlite3_exec(database, statusQuery.c_str(), callback, 0, 0);
			if (error) {
				cout << "Check: Can not get work status (" << error << ")" << endl;
				return 1;
			}
			sqlite3_close(database);
			if (workStatus=="FINISHED") break;
		}
	}
	
	return 0;
}
