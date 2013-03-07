#include <sqlite3.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <bitset>
#include <vector>
#include <map>
#include <sys/wait.h>

using namespace std;

//Initialize datastructures
time_t start = time(NULL);
bitset<79154950> vecList [240];
vector<vector <unsigned int > > BScounts (79154950);
vector<vector <unsigned short > > BSlocations (79154950);
bitset<79154950> ANDvec;
bitset<79154950> ORvec;

int worksLimit=1;
unsigned int processesLimit=1;
string workID_start="";
string motifFilePath_start="";
string outFilePath_start="";
static int callbackWaiting(void *NotUsed, int argc, char **argv, char **azColName) {
	workID_start=argv[0];
	motifFilePath_start=argv[1];
	outFilePath_start=argv[2];
	return 0;
}

int numOfRunning;
static int callbackRunning(void *NotUsed, int argc, char **argv, char **azColName) {
	numOfRunning=atoi( argv[0]);
	return 0;
}

int runCountWork(string work_id, string motifFilePath_start, string outFilePath_start, map<char,int> aminoPosMap) {
	time_t start = time(NULL);
	string line;
	vector<string> motifList;
	
	//Read input motifs
	ifstream motifFile (motifFilePath_start.c_str());
	if (motifFile.is_open()) {
		while ( getline(motifFile, line) ) {
			motifList.push_back(line);
		}
		motifFile.close();
	} else {
		return 1;
	}
	
	//Calculate counts and write output
	ofstream resFile (outFilePath_start.c_str(), ios::trunc);
	if (resFile.is_open()) {
		if (motifList.size() < processesLimit) {
			//Single process
			cout << "Counting started (id: " << work_id << ", processes: 1)" << endl;
			for (unsigned int i=0; i < motifList.size(); i++) { //iga motiivi kohta
				ORvec.reset();
				for (unsigned int j=0; j < 13-motifList[i].size(); j++) { //iga võimaliku psitsiooni kohta
					ANDvec.set();
					for (unsigned int k=0; k < motifList[i].size(); k++) { // iga tähe kohta motiivis
						if (motifList[i][k]!='.') {
							ANDvec&=vecList[aminoPosMap[motifList[i][k]]+(k+j)*20];
						}
					}
					ORvec|=ANDvec;
				}
				unsigned int resList[1306] = {0};
				for (unsigned int l=0; l < 79154950; l++) {
					if (ORvec[l]==1) {
						for (unsigned int m=0; m < BSlocations[l].size(); m++) {
							resList[BSlocations[l][m]]=resList[BSlocations[l][m]]+BScounts[l][m];
						}
					}
				}
				stringstream resOut;
				resOut << motifList[i];
				for (unsigned int n=0; n < 1306; n++) {
					resOut << "\t" << resList[n];
				}
				resOut << endl;
				resFile << resOut.str();
			}
			resFile.close();
		} else {
			//multiprocess
			cout << "Counting started (id: " << work_id << ", processes: " << processesLimit << ")" << endl;
			int motifs_per_process=motifList.size()/processesLimit;
			int pfds[processesLimit][2];
			for (unsigned int o=0; o < processesLimit; o++) {
				pipe(pfds[o]);
				pid_t PID = fork();
				if (PID > 0) {
					continue;
				} else if (PID == 0) {
					if (o == 0) {
						//First sub (can write directly to pipe)
						for (int i=0; i < motifs_per_process; i++) { //iga motiivi kohta
							ORvec.reset();
							for (unsigned int j=0; j < 13-motifList[i].size(); j++) { //iga võimaliku psitsiooni kohta
								ANDvec.set();
								for (unsigned int k=0; k < motifList[i].size(); k++) { // iga tähe kohta motiivis
									if (motifList[i][k]!='.') {
										ANDvec&=vecList[aminoPosMap[motifList[i][k]]+(k+j)*20];
									}
								}
								ORvec|=ANDvec;
							}
							unsigned int resList[1306] = {0};
							for (unsigned int l=0; l < 79154950; l++) {
								if (ORvec[l]==1) {
									for (unsigned int m=0; m < BSlocations[l].size(); m++) {
										resList[BSlocations[l][m]]=resList[BSlocations[l][m]]+BScounts[l][m];
									}
								}
							}
							stringstream resOut;
							resOut << motifList[i];
							for (unsigned int n=0; n < 1306; n++) {
								resOut << "\t" << resList[n];
							}
							resOut << '\n';
							string tempResOutStr=resOut.str();
							for (unsigned int c=0; c < tempResOutStr.size(); c++) {
								write(pfds[o][1], tempResOutStr.substr(c,1).c_str(), 1);
							}
						}
						write(pfds[o][1], "!", 1);
						
					} else if (o == processesLimit-1) {
						//Last sub (takes all excess motifs)
						stringstream resOut;
						for (unsigned int i=motifs_per_process*o; i < motifList.size(); i++) { //iga motiivi kohta
							ORvec.reset();
							for (unsigned int j=0; j < 13-motifList[i].size(); j++) { //iga võimaliku psitsiooni kohta
								ANDvec.set();
								for (unsigned int k=0; k < motifList[i].size(); k++) { // iga tähe kohta motiivis
									if (motifList[i][k]!='.') {
										ANDvec&=vecList[aminoPosMap[motifList[i][k]]+(k+j)*20];
									}
								}
								ORvec|=ANDvec;
							}
							unsigned int resList[1306] = {0};
							for (unsigned int l=0; l < 79154950; l++) {
								if (ORvec[l]==1) {
									for (unsigned int m=0; m < BSlocations[l].size(); m++) {
										resList[BSlocations[l][m]]=resList[BSlocations[l][m]]+BScounts[l][m];
									}
								}
							}
							resOut << motifList[i];
							for (unsigned int n=0; n < 1306; n++) {
								resOut << "\t" << resList[n];
							}
							resOut << endl;
						}
						string tempResOutStr=resOut.str();
						for (unsigned int c=0; c < tempResOutStr.size(); c++) {
							write(pfds[o][1], tempResOutStr.substr(c,1).c_str(), 1);
						}
						write(pfds[o][1], "!", 1);
					} else {
						//Middle subs
						stringstream resOut;
						for (unsigned int i=motifs_per_process*o; i < motifs_per_process*(o+1); i++) { //iga motiivi kohta
							ORvec.reset();
							for (unsigned int j=0; j < 13-motifList[i].size(); j++) { //iga võimaliku psitsiooni kohta
								ANDvec.set();
								for (unsigned int k=0; k < motifList[i].size(); k++) { // iga tähe kohta motiivis
									if (motifList[i][k]!='.') {
										ANDvec&=vecList[aminoPosMap[motifList[i][k]]+(k+j)*20];
									}
								}
								ORvec|=ANDvec;
							}
							unsigned int resList[1306] = {0};
							for (unsigned int l=0; l < 79154950; l++) {
								if (ORvec[l]==1) {
									for (unsigned int m=0; m < BSlocations[l].size(); m++) {
										resList[BSlocations[l][m]]=resList[BSlocations[l][m]]+BScounts[l][m];
									}
								}
							}
							resOut << motifList[i];
							for (unsigned int n=0; n < 1306; n++) {
								resOut << "\t" << resList[n];
							}
							resOut << '\n';
						}
						string tempResOutStr=resOut.str();
						for (unsigned int c=0; c < tempResOutStr.size(); c++) {
							write(pfds[o][1], tempResOutStr.substr(c,1).c_str(), 1);
						}
						write(pfds[o][1], "!", 1);
					}
					return 2;
				}
			}
			
			//Read pipes and write output
			for (unsigned int p=0; p < processesLimit; p++) {
				char buf[1];
				read(pfds[p][0], buf, 1);
				while (buf[0]!='!') {
					resFile << buf[0];
					read(pfds[p][0], buf, 1);
				}
			}
			
			resFile.close();
		}
	} else {
		return 1;
	}
	cout << "  Counting done (id:" << work_id << ", motifs:" << motifList.size() << ", time:" << difftime(time(NULL),start) << ")" << endl;
	return 0;
}

int main(int argc, char *argv[]) {
	cout << "Init done. PID: " << getpid() << endl;
	//Database creation/check
	int error = 0;
	sqlite3 *database;
	error = sqlite3_open("workListDB.sqlite", &database);
	if (error) {
		cout << "Can not open/create database (" << error << ") exiting!"<<endl;
		return 1;
	}
	error = sqlite3_exec(database, "CREATE TABLE IF NOT EXISTS workList (workID INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT, motifFilePath TEXT, outFilePath TEXT)", 0, 0, 0);
	if (error) {
		cout << "Can not create/check worklist table (" << error << ") exiting!" << endl;
		sqlite3_close(database);
		return 1;
	}
	sqlite3_close(database);
	cout << "Database creation/check done." << endl;
	
	//Create position map of letters
	map<char,int> aminoPosMap;
	aminoPosMap['A']=0;
	aminoPosMap['C']=1;
	aminoPosMap['D']=2;
	aminoPosMap['E']=3;
	aminoPosMap['F']=4;
	aminoPosMap['G']=5;
	aminoPosMap['H']=6;
	aminoPosMap['I']=7;
	aminoPosMap['K']=8;
	aminoPosMap['L']=9;
	aminoPosMap['M']=10;
	aminoPosMap['N']=11;
	aminoPosMap['P']=12;
	aminoPosMap['Q']=13;
	aminoPosMap['R']=14;
	aminoPosMap['S']=15;
	aminoPosMap['T']=16;
	aminoPosMap['V']=17;
	aminoPosMap['W']=18;
	aminoPosMap['Y']=19;
	
	//Load big summary table
	cout << "Loading BS..." << endl;
	string line;
	int indexCount=0;
	int lineNumber=0;
	ifstream BS ("/group/work/project/protobios/2013_01_28_BS_with29to36/dat/purifiedBS/bigSummary_02_13.txt");
	if (BS.is_open()) {
		string peptide;
		string count;
		while ( getline(BS, line) ) {
			istringstream ss( line );
			getline(ss, peptide, '\t');
			
			//Fill vecList for current line
			vecList[aminoPosMap[peptide[0]]][lineNumber]=1;
			vecList[aminoPosMap[peptide[1]]+20][lineNumber]=1;
			vecList[aminoPosMap[peptide[2]]+40][lineNumber]=1;
			vecList[aminoPosMap[peptide[3]]+60][lineNumber]=1;
			vecList[aminoPosMap[peptide[4]]+80][lineNumber]=1;
			vecList[aminoPosMap[peptide[5]]+100][lineNumber]=1;
			vecList[aminoPosMap[peptide[6]]+120][lineNumber]=1;
			vecList[aminoPosMap[peptide[7]]+140][lineNumber]=1;
			vecList[aminoPosMap[peptide[8]]+160][lineNumber]=1;
			vecList[aminoPosMap[peptide[9]]+180][lineNumber]=1;
			vecList[aminoPosMap[peptide[10]]+200][lineNumber]=1;
			vecList[aminoPosMap[peptide[11]]+220][lineNumber]=1;
			
			//Fill BScounts and BSlocations for current line
			indexCount=0;
			while (!ss.eof()) {
				getline(ss, count, '\t');
				if (count!="0") {
					BScounts[lineNumber].push_back( atoi( count.c_str() ) );
					BSlocations[lineNumber].push_back( indexCount );
				}
				indexCount=indexCount+1;
			}
			lineNumber=lineNumber+1;
			
			//For testing, comment out in production
			// if (lineNumber==100001) {
				// break;
			// }
		}
		BS.close();
	} else {
		cout << "Can not open big summary... exiting." << endl;
		return 1;
	}
	cout << "  done (" << difftime(time(NULL),start) << ")" << endl << endl;
	
	//Check status of works (interval 60s), infinate loop untill manager is killed
	while(1) {
		sleep(60);
		error = sqlite3_open("workListDB.sqlite", &database);
		if (error) {
			cout << "Check for work: Error opening database (" << error << ")" << endl;
			continue;
		}
		sqlite3_busy_timeout(database, 60000);
		//Get first 'Waiting' work, go to next loop if no works waiting
		error = sqlite3_exec(database, "SELECT workID, motifFilePath, outFilePath FROM workList WHERE status = \'Waiting\' ORDER BY workID LIMIT 1", callbackWaiting, 0, 0);
		if (error) {
			cout << "Check for work: Error geting waiting jobs (" << error << ")" << endl;
			sqlite3_close(database);
			continue;
		}
		if (workID_start=="") {
			sqlite3_close(database);
			continue;
		}
		
		//Get number of running works
		error = sqlite3_exec(database, "SELECT COUNT(*) FROM workList WHERE status = \'Running\'", callbackRunning, 0, 0);
		if (error) {
			cout << "Check for work: Error geting running jobs (" << error << ")" << endl;
			sqlite3_close(database);
			continue;
		}
		sqlite3_close(database);
		
		//If number of running works is below the limit then start new work
		if (numOfRunning<worksLimit) {
			pid_t childPID_1;
			childPID_1 = fork();
			if ( childPID_1 > 0 ) {
				waitpid(childPID_1, NULL, 0);
			} else if (childPID_1==0) {
				pid_t childPID_2;
				childPID_2 = fork();
				if (childPID_2 > 0) {
					exit(0);
				} else if (childPID_2==0) {
					string setRunningQuery;
					stringstream setR_ss;
					setR_ss << "UPDATE workList SET status=\'Running\' where workID = " << workID_start;
					setRunningQuery = setR_ss.str();
					
					string setFinishedQuery;
					stringstream setF_ss;
					setF_ss << "UPDATE workList SET status=\'Finished\' where workID = " << workID_start;
					setFinishedQuery = setF_ss.str();
					
					string setErrorQuery;
					stringstream setE_ss;
					setE_ss << "UPDATE workList SET status=\'Error\' where workID = " << workID_start;
					setErrorQuery = setE_ss.str();
					
					sqlite3 *database;
					error = sqlite3_open("workListDB.sqlite", &database);
					if (error) {
						cout << "Update work: Error opening database (" << error << ")" << endl;
						return 1;
					}
					sqlite3_busy_timeout(database, 60000);
					error = sqlite3_exec(database, setRunningQuery.c_str(), 0, 0, 0);
					if (error) {
						cout << "Update work: Error seting status \'Running\' (" << error << ") " << workID_start << endl;
						sqlite3_close(database);
						return 1;
					}
					sqlite3_close(database);
					
					int runCountWork_exitCode = runCountWork(workID_start, motifFilePath_start, outFilePath_start, aminoPosMap);
					
					error = sqlite3_open("workListDB.sqlite", &database);
					if (error) {
						cout << "Update work: Error opening database (" << error << ")" << endl;
						return 1;
					}
					sqlite3_busy_timeout(database, 60000);
					
					if (runCountWork_exitCode==0) {
						error = sqlite3_exec(database, setFinishedQuery.c_str(), 0, 0, 0);
						if (error) {
							cout << "Update work: Error seting status \'Finished\' (" << error << ") " << workID_start << endl;
							sqlite3_close(database);
							return 1;
						}
						sqlite3_close(database);
						return 0;
					} else if (runCountWork_exitCode==1) {
						error = sqlite3_exec(database, setErrorQuery.c_str(), 0, 0, 0);
						if (error) {
							cout << "Update work: Error seting status \'Error\' (" << error << ") " << workID_start << endl;
							sqlite3_close(database);
							return 1;
						}
						sqlite3_close(database);
						return 1;
					} else {
						return 0;
					}
					
				} else {
					cout << "Second new work fork failed" << endl;
				}
			} else {
				cout << "First new work fork failed" << endl;
			}
		}
		
		workID_start="";
		motifFilePath_start="";
		outFilePath_start="";
	}
	return 0;
}
