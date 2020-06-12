## greet
* greet
  - utter_greet_with_buttons
  - action_restart


## faq question asked, FAQ was answered correctly
* faq_ari OR faq_ccpa OR faq_ebill_disable OR faq_escrow OR faq_gi OR faq_heloc OR faq_ii OR faq_pdp OR faq_pi OR faq_pt OR faq_rlt OR faq_sm OR faq_tax_statement
  - action_trigger_faq
  - action_restart



## dynamic query from canned training sheet
* canned_generic_escrow_details OR canned_generic_escrow_disbursal OR canned_generic_FICO OR canned_generic_outst_balance OR canned_not_recv_bill_st OR canned_pmt_breakdown OR canned_pmt_change_dd OR canned_pmt_change_reason OR canned_pmt_late_fee OR canned_pmt_nsf OR canned_pmt_other_fees OR canned_generic_due_date
  - action_get_canned_dynamic_response
  - action_restart

## info about covid-19
* covid_support
  - utter_covid_support


## user wants to pay
* user_wants_pay
  - utter_payment_options


## user selected otd payment mail
* otd_mail_selected
  - utter_otd_mail

## user wants to pay srp
* srp_payment_options
  - utter_srp_payment_options

## user wants to pay otd
* otd_payment_options
  - utter_otd_payment_options


## user selected otd payment phone
* otd_phone_selected
  - utter_otd_phone


## user selected otd payment online
* otd_chat_selected
  - otd_payment_form
  - action_restart


## user selected srp payment mail
* srp_mail_selected
  - utter_srp_mail


## user selected srp payment online
* srp_online_selected
  - utter_srp_online


## user selected srp payment in chat
* srp_chat_selected
  - srp_payment_form
  - action_restart


## user liked
* intent_user_liked
  -  utter_happy


## user disliked
* intent_user_disliked
  -  utter_apologize