#! /usr/intel/bin/python


import os
import re
import subprocess
import sys
import time

def is_test_done(rpt_file):
  cmd = "lsti "+rpt_file;
  output = subprocess.check_output(cmd, shell=True)
  
  
  output = output.decode("ascii",errors="ignore")
  
  #print(output);
  total=0;
  no_status = 0;
  
  line_num=0;
  lines = output.splitlines();
  for line in lines:
    if( "Pass Fail No Status Total % Passing" in line ):
      #print(lines[line_num+2]);
      num_array = lines[line_num+2].split(); 
      total = num_array[3];
      no_status = num_array[2];
      #print("total "+total+" no_status "+no_status);
    line_num=line_num+1;  
  return (no_status=='0'); 

def get_lsti_summary(rpt_file):
  cmd = "lsti -l "+rpt_file;

  output = subprocess.check_output(cmd, shell=True);
  #output = subprocess.check_output(cmd, shell=True);
  
  
  output = output.decode("ascii",errors="ignore")
  
  lines = output.splitlines();
  summary = '';
  found = False ;
  for line in lines:
    if( "Bucket Count Bucket Name" in line ):
      found = True;
    if(found):
      summary= summary + line + "\n";
      #if( len(line)<4):
      #  found = 0;
  return summary; 

def get_lsti_rb_summary(rpt_file):
  cmd = "lsti -rb -l "+rpt_file;
  output = subprocess.check_output(cmd, shell=True)
  
  
  output = output.decode("ascii",errors="ignore")
  
  line_num=0;
  lines = output.splitlines();
  summary = '';
  found = False ;
  for line in lines:
    if( "Bucket Count Bucket Name" in line ):
      found = True;
      summary_begin = line; 
    if(found):
      if(line_num<75):
        summary= summary + line + "\n";
      else:
        summary= summary + "\n too many failures to put inside email; go to the result directory for details\n";
        break;
      line_num=line_num+1;  
  return summary; 

##############################################################

email_list = "weilin.cao@intel.com saravanan.egambaram@intel.com rohit1.singh@intel.com rama.krishna.vyata@intel.com parth.a.patel@intel.com  keytaek.lee@intel.com kailesh.bavaria@intel.com jim.ming.lim@intel.com  brandon.l.smalley@intel.com adelene.kah.jia.huong@intel.com";
#email_list = "weilin.cao@intel.com";
results_dir = sys.argv[1];
results_dir = subprocess.check_output("realpath "+results_dir, shell=True).decode('utf-8').strip() + "/";
results_base = subprocess.check_output( ("basename " + results_dir), shell=True).decode('utf-8').strip();

rpt =results_dir + "*.rpt" ;
minute=0;
while(is_test_done(rpt)==False and minute < (24*60) ):
  time.sleep(60*10);
  #print("tests not yet completed");
  minute += 10;

if (minute< (24*60) ):
  print("all test completed, sending emails to subscribers");
else:
  print("tests been running over 24 hours; not all test completed, sending emails to subscribers");
#print(get_lsti_summary(rpt) );
content = "Please see the result directory at:"+results_dir +"\nBelow is the lsti summary:\n\n"+ get_lsti_summary(rpt) + "\n\nBucket Details:\n\n" + get_lsti_rb_summary(rpt)  +  "\n\n\nThis is an automated msg, please reach out to weilin.cao@intel.com for any question\n";
content = content.replace("\n","\\n").replace("\t","\\t").replace('"',"'").replace("`","");
cmd = 'echo -e "'+ content  +  '" | '+ 'mail -s "Regression Result for '+ results_base + '" '+ email_list;
os.system(cmd);

