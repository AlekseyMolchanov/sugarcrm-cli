usage: sugar_cli [--help] {account,contact,call,meeting,opportunity} \
                          {show,get,create,update,delete,cascade_create,cascade_delete,fields} \
                          --required=arguments [--optional=arguments]

positional arguments <Module>:
  {account,contact,call,meeting,opportunity}
                        
    account             Module: Accounts
    contact             Module: Contacts
    call                Module: Calls
    meeting             Module: Meetings
    opportunity         Module: Opportunities

positional arguments:
  {show,get,create,update,delete,cascade_create,cascade_delete,fields}
                        
    show                Show action: show all items or search by some fild value
    >./sugar_cli.py <Module> show [--optional=arguments]


    get                 Get by id action
    the following arguments are required: --id
    >./sugar_cli.py <Module> get --id ID 
    

    CREATE              
    Create new object 
    >./sugar_cli.py <Module> create --required=arguments [--optional=arguments]
    
    module:                arguments:

    account                --account_type
                           {Analyst,Competitor,Customer,Integrator,Investor,
                            Other,Partner,Press,Prospect,Reseller}
                           --name NAME
                           --billing_address_street BILLING_ADDRESS_STREET
                           --billing_address_postalcode BILLING_ADDRESS_POSTALCODE 
                           --billing_address_city BILLING_ADDRESS_CITY 
                           --phone_office PHONE_OFFICE
                           --industry INDUSTRY 
                           [--billing_address_country BILLING_ADDRESS_COUNTRY]
                           [--id ID]

    contact                --first_name FIRST_NAME 
                           --last_name LAST_NAME
                           --title TITLE 
                           --primary_address_street PRIMARY_ADDRESS_STREET 
                           --primary_address_city PRIMARY_ADDRESS_CITY 
                           --primary_address_postalcode PRIMARY_ADDRESS_POSTALCODE 
                           --phone_home PHONE_HOME
                           --phone_mobile PHONE_MOBILE 
                           --phone_other PHONE_OTHER 
                           --phone_work PHONE_WORK 
                           --salutation SALUTATION 
                           --email1 EMAIL1 
                           --account_id ACCOUNT_ID
                           [--id ID] 

    call                   --name NAME 
                           --date_start DATE_START
                           --parent_type PARENT_TYPE
                           --parent_id PARENT_ID 
                           [--id ID] 

    meeting                --name NAME 
                           --description DESCRIPTION
                           --date_start DATE_START 
                           --date_end DATE_END
                           --parent_type PARENT_TYPE
                           --parent_id PARENT_ID 
                           [--id ID] 

    opportunity            --name NAME 
                           --amount AMOUNT
                           --date_closed DATE_CLOSED 
                           --account_id ACCOUNT_ID
                           [--account_name ACCOUNT_NAME] 
                           [--id ID]

    task                   --name NAME 
                           --description DESCRIPTION
                           --date_start DATE_START 
                           --date_end DATE_END
                           --priority {High,Low,Medium} 
                           --contact_id CONTACT_ID
                           --parent_id PARENT_ID 
                           --parent_type PARENT_TYPE
                           [--date_modified DATE_MODIFIED] 
                           [--id ID] 
                           

    UPDATE              
    Update model fields by id
    the following arguments are required: --id
    >./sugar_cli.py <Module> update --id ID [--optional=arguments] 
    

    DELETE              
    Delete by id
    the following arguments are required: --id 
    >./sugar_cli.py <Module> delete --id ID


    CASCADE_DELETE      
    Cascade delete by id
    the following arguments are required: --id 
    >./sugar_cli.py <Module> cascade_delete --id ID


    CASCADE_CREATE      
    Cascade create fake data objects
    the following arguments are required: --count 
    >./sugar_cli.py <Module> cascade_create --count=<int>

    FIELDS
    Get information abount module model, 
    get fields by type: default module_fields
    >./sugar_cli.py <Module> fields
    >./sugar_cli.py <Module> fields --type=module_fields
    get field description
    >./sugar_cli.py <Module> fields --type=<str> --field contact_id
     


optional arguments:
  --help                show this help message and exit

