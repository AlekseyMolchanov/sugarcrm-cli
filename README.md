# Sugar CRM command line interface (4.1 REST API)

[![CircleCI](https://circleci.com/gh/AlekseyMolchanov/sugarcrm-cli.svg?style=svg)](https://circleci.com/gh/AlekseyMolchanov/sugarcrm-cli)
[![codecov](https://codecov.io/gh/AlekseyMolchanov/sugarcrm-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/AlekseyMolchanov/sugarcrm-cli)

# Install
  
    1) clone repository
    2) install requirements

      pip install -r requirements.txt

    3) define Environment Variables : SUGAR_CRM_URL, SUGAR_CRM_USERNAME and SUGAR_CRM_PASSWORD
    
      export SUGAR_CRM_URL=http://...../service/v4_1/rest.php
      export SUGAR_CRM_USERNAME='username'
      export SUGAR_CRM_PASSWORD='password'



# Usage
  
  ./sugar_cli {module} {action} (--params ...... +)
  
  Modules:
  
    * Account
    * Contact  
    * Meeting
    * Call
    * Opportunitie
  
  Actions:
    
    * show
    * get
    * create
    * update
    * delete
    * cascade_delete
