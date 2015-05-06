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
        
    // Start constructing the header of the message to send to the server:
    TString hdr = "POST /";
    hdr += url.GetFile();
    hdr += " HTTP/1.0";
    hdr += "\r\n";
    hdr += "From: ";
    if( uinfo.get() ) {
       hdr += uinfo->fUser + "@";
    } else {
       hdr += "unknown@";
    }
    hdr += gSystem->HostName();
    hdr += "\r\n";
    hdr += "User-Agent: xAODRootAccess\r\n";
    hdr += "Content-Type: application/json\r\n";
    hdr += "Content-Length: ";
        
    // Now construct the message payload:
    //TString pld = ;
    
    TString pld = "[{";
    pld += " \"body\" : \"{\"accessedFiles\": [\"file1\",\"file2\"]}\" ";
    pld += ", \"headers\": {\"timestamp\": \"434324343\", \"host\": \"random_host.example.com\"}";
    pld += "}]"; 
        
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
