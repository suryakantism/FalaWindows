## greet a logged in user
* greet
  - utter_greet_with_buttons
  - action_restart


## faq question asked, FAQ was answered correctly
* faq_ari OR faq_ccpa OR faq_escrow OR faq_gi OR faq_heloc OR faq_ii OR faq_pdp OR faq_pi OR faq_pt OR faq_rlt OR faq_sm
  - action_trigger_faq


## Admin request to train data
* train_data
  - action_get_is_admin
  - slot{"is_admin" : true}
  - faq_fix_form
  - utter_confirm_fix_faq
  - action_restart


## Admin request to train data
* train_data
  - action_get_is_admin
  - slot{"is_admin" : false}
  - utter_admin_detection_failed
  - action_restart


## dynamic query from canned training sheet
* canned_generic_MDA_breakup OR canned_pmt_change_dd OR canned_generic_due_date OR canned_generic_FICO OR canned_pmt_other_fees OR canned_pmt_late_fee OR canned_pmt_nsf OR canned_generic_outst_balance OR canned_pmt_breakdown OR canned_generic_escrow_disbursal OR canned_pmt_change_reason
  - action_get_canned_dynamic_response


## user liked
* intent_user_liked
  - utter_happy


## user disliked
* intent_user_disliked
  - utter_apologize