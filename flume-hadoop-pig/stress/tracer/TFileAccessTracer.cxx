#include <memory>

// ROOT include(s):
#include <TSystem.h>
#include <TFile.h>
#include <TError.h>
#include <TUrl.h>
#include <TSocket.h>

static ::TUrl url( SERVER_ADDRESS );
	      ::TSocket socket( url.GetHost(), url.GetPort() );
	      if( ! socket.IsValid() ) {
	         ::Error( "xAOD::TFileAccessTracer::~TFileAccessTracer",
	                  XAOD_MESSAGE( "No valid socket could be established to: %s" ),
	                  SERVER_ADDRESS );
	         return;
	      }

// Get some info about the user:
// 55	      std::unique_ptr< ::UserGroup_t > uinfo( gSystem->GetUserInfo() );
// 56	
// 57	      // Start constructing the header of the message to send to the server:
// 58	      ::TString hdr = "POST /";
// 59	      hdr += url.GetFile();
// 60	      hdr += " HTTP/1.0";
// 61	      hdr += "\r\n";
// 62	      hdr += "From: ";
// 63	      if( uinfo.get() ) {
// 64	         hdr += uinfo->fUser + "@";
// 65	      } else {
// 66	         hdr += "unknown@";
// 67	      }
// 68	      hdr += gSystem->HostName();
// 69	      hdr += "\r\n";
// 70	      hdr += "User-Agent: xAODRootAccess\r\n";
// 71	      hdr += "Content-Type: application/json\r\n";
// 72	      hdr += "Content-Length: ";
// 73	
// 74	      // Now construct the message payload:
// 75	      ::TString pld = "{\"accessedFiles\": [";
// 76	      bool first = true;
// 77	      for( auto& info : m_accessedFiles ) {
// 78	         if( ! first ) {
// 79	            pld += ", ";
// 80	         }
// 81	         pld += "[\"" + info.filePath + "\",\"" + info.fileName + "\"]";
// 82	         first = false;
// 83	      }
// 84	      pld += "]}";
// 85	
// 86	      // Now finish constructing the header, and merge the two into a single
// 87	      // message:
// 88	      hdr += TString::Format( "%i", pld.Length() );
// 89	      hdr += "\r\n\r\n";
// 90	      const ::TString msg = hdr + pld;
//   // A debug message for the time being:
//   93	      Info( "xAOD::TFileAccessTracer::~TFileAccessTracer",
//   94	            "Sending message:\n\n%s", msg.Data() );
//   95	
//   96	      // Send the message:
//   97	      if( socket.SendRaw( msg.Data(), msg.Length() ) < 0 ) {
//   98	         ::Error( "xAOD::TFileAccessTracer::~TFileAccessTracer",
//   99	                  XAOD_MESSAGE( "Failed to send message: %s" ), msg.Data() );
//   100	         return;
//   101	      }
//   102	   }
//   103	
//   104	   /// This function is called by TEvent to record which files were read from
//   105	   /// during the job.
//   106	   ///
//   107	   /// @param file The file object that is being read from
//   108	   ///
//   109	   void TFileAccessTracer::add( const ::TFile& file ) {
//   110	
//   111	      // Remember this file:
//   112	      m_accessedFiles.insert(
//   113	         AccessedFile{ gSystem->DirName( file.GetName() ),
//   114	                       gSystem->BaseName( file.GetName() ) } );
//   115	
//   116	      // Return gracefully:
//   117	      return;
//   118	   }
//    bool TFileAccessTracer::AccessedFile::
//    129	   operator< ( const AccessedFile& rhs ) const {
//    130	
//    131	      if( filePath != rhs.filePath ) {
//    132	         return filePath < rhs.filePath;
//    133	      }
//    134	      if( fileName != rhs.fileName ) {
//    135	         return fileName < rhs.fileName;
//    136	      }
//    137	
//    138	      return false;
//    139	   }
//    140	
