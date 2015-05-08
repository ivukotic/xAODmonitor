#include <memory>
#include <stdlib.h>
#include <iostream>

// ROOT include(s):
#include <TSystem.h>
#include <TFile.h>
#include <TError.h>
#include <TUrl.h>
#include <TSocket.h>

using namespace std;

class AccessedFile {
   public:
      /// The full path to the file
      TString filePath;
      /// The name of the file
      TString fileName;
};


int main(int argc, char **argv){
    
    static const char* SERVER_ADDRESS = "http://hadoop-dev.mwt2.org:18080";
    static TUrl url( SERVER_ADDRESS );
    TSocket socket( url.GetHost(), url.GetPort() );

    if( ! socket.IsValid() ) {
        cout<<"No valid socket could be established to" << endl;
        return 1;
    }

    // Get some info about the user:
    unique_ptr< UserGroup_t > uinfo( gSystem->GetUserInfo() );
        
        
     vector< AccessedFile > m_accessedFiles;   
     m_accessedFiles.push_back(AccessedFile{ TString("/myFilePath/a/b/c/"),  TString("myFileName.root")  } );
     m_accessedFiles.push_back(AccessedFile{ TString("/myFilePath/c/b/a/"),  TString("myFileName1.root")  } );
                      
    // Start constructing the header of the message to send to the server:
    TString hdr = "POST /";
    hdr += url.GetFile();
    hdr += " HTTP/1.0";
    hdr += "\r\n";
    hdr += "From: ";
    hdr += gSystem->HostName();
    hdr += "\r\n";
    hdr += "User-Agent: xAODRootAccess\r\n";
    hdr += "Content-Type: application/json\r\n";
    hdr += "Content-Length: ";
        
    // Now construct the message payload:
    
    TString pld = "[{";
    pld += "\"body\": \"{\\\"accessedFiles\\\": [";
    bool first = true;
    for( auto& info : m_accessedFiles ) {
       if( ! first ) {
          pld += ", ";
       }
       pld += "[\\\"" + info.filePath + "\\\",\\\"" + info.fileName + "\\\"]";
       first = false;
    }
    pld += "],";
    const xAOD::ReadStats& rs = xAOD::IOStats::instance().stats();
    pld += " \\\"accessedContainers\\\": [";
    first = true;
    for( const auto& bs : rs.containers() ) {
       if( ! bs.second.readEntries() ) {
          continue;
       }
       if( ! first ) {
          pld += ", ";
       }
       pld += "{\\\"name\\\": \\\"";
       pld += bs.second.GetName();
       pld += "\\\", \\\"readEntries\\\": ";
       pld += bs.second.readEntries();
       pld += "}";
       first = false;
    }
    pld += "], ";
    pld += " \\\"accessedBranches\\\": [";
    first = true;
    for( const auto& branch : rs.branches() ) {
       for( const xAOD::BranchStats* bs : branch.second ) {
          if( ( ! bs ) || ( ! bs->readEntries() ) ) {
             continue;
          }
          if( ! first ) {
             pld += ", ";
          }
          pld += "{\\\"name\\\": \\\"";
          pld += bs->GetName();
          pld += "\\\", \\\"readEntries\\\":";
          pld += bs->readEntries();
          pld += "}";
          first = false;
       }
    }
    pld += "]}, ";
    pld += "\"headers\": {\"timestamp\": \"";
    pld += TTimeStamp().GetSec();
    pld += "\", \"host\": \"";
    pld += gSystem->HostName();
    pld += "\"}}]";
    
        
    // Now finish constructing the header, and merge the two into a single message:
    hdr += TString::Format( "%i", pld.Length() );
    hdr += "\r\n\r\n";
    const ::TString msg = hdr + pld;
    
    // A debug message for the time being:
   	cout<< msg.Data()<<endl;
   	
   	// Send the message:
   	if( socket.SendRaw( msg.Data(), msg.Length() ) < 0 ) {
   	  cout<< "Failed to send message."<<endl;
   	}
   	   
   	
    return 0;    	
}
