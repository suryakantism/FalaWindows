## greet
* greet
  - utter_greet_with_buttons
  - action_restart


## faq question asked, FAQ was answered correctly
* faq_ari OR faq_ccpa OR faq_escrow OR faq_gi OR faq_heloc OR faq_ii OR faq_pdp OR faq_pi OR faq_pt OR faq_rlt OR faq_sm
  - action_trigger_faq



## dynamic query from canned training sheet
* canned_generic_MDA_breakup OR canned_pmt_change_dd OR canned_generic_due_date OR canned_generic_FICO OR canned_pmt_other_fees OR canned_pmt_late_fee OR canned_pmt_nsf OR canned_generic_outst_balance OR canned_pmt_breakdown OR canned_escrow_disbursal OR canned_pmt_change_reason
  - utter_ask_login


## info about covid-19
* covid_support
  - utter_covid_support


## new customer 
* new_customer
  - utter_new_customer


## new heloc customer
* new_heloc_customer
  - utter_new_heloc_customer


## user liked
* intent_user_liked
  -  utter_happy


## user disliked
* intent_user_disliked
  -  utter_apologize

  