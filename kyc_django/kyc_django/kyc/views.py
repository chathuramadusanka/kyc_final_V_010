import smtplib
import random
import urllib
from email.message import EmailMessage
from django.contrib.messages.api import success

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Kyc_Info, Kyc_Infotemp, Id_Info, Image, Kyc_Reject, HistoricalKyc_Info, Kyc_front, Social_core
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from .forms import update_forms, accept_form, ImageForm, reject_forms
import numpy as np
# import alert

# import alert
#
# if __name__ == '__main__':
#     alert.email_alert("password", "in kyc", "dmhashanmd@gmail.com")
#
#



# define method for calling pages
# -----------------------------------------------------------------------------------------------------------------------


def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "kyc064810@gmail.com"
    msg['from'] = user
    password = "qtmwyfuyknyvvtag"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()



def index(request):
    return render(request, 'kyc/index.html')

def verify(request):

    # if request.session.get('id'):

    # id = format(request.session.get('id'))

    # if request.GET[id]:
    # id=request.GET['id']
    if request.method == "POST":
        input_number = request.POST["code"]
        
        print(input_number)
        # previous method Kyc_Infotemp.objects
        if Kyc_Infotemp.objects.filter(email_add_verification=input_number, id=saved_id_for_email_vari).exists():
            Kyc_Infotemp.objects.filter(email_add_verification=input_number, id=saved_id_for_email_vari).update(email_varified_temp="True")
            messages.success(request, "verified sucessfully")
            return render(request, "kyc/search.html")

        else:
            messages.error(request, "Invalid code, Please enter the received code")

        

    """dbObj = Kyc_Infotemp.objects.get(id=id)
    dbNum = dbObj.email_add_verification
    emNum = request.GET["ecode"]
    if(dbNum==emNum):
        Kyc_Infotemp.objects.filter(id=id).update(email_add_verification='verifiede')
        print("ok")
        return render(request,'kyc/ok.html')"""
    return render(request, "kyc/verify.html")

def verify2(request):

    # # if request.session.get('id'):
    #
    # # id = format(request.session.get('id'))
    #
    # # if request.GET[id]:
    # id=request.GET['id']
    #
    # dbObj = Kyc_Infotemp.objects.get(id=id)
    # dbNum = dbObj.email_add_verification
    # emNum = request.GET["ecode"]
    # if(dbNum==emNum):
    #     Kyc_Infotemp.objects.filter(id=id).update(email_add_verification='verifiede')
    #     print("ok")
    messages.success(request, 'Mobile number verified')
    return render(request,'kyc/index.html')

def account(request):
    return render(request, 'kyc/(2nd)AccEmp.html')


def personal(request):
    return render(request, 'kyc/(3rd)Declaration.html')


def office(request):
    return render(request, 'kyc/(4th)office.html')


# defining function to filter and display flagged records in update.html
def update(request):
    result = Kyc_Infotemp.objects.filter(green_flag_temp=True)
    result2 = Kyc_Infotemp.objects.filter(blue_flag_temp=True)
    result3 = Kyc_Infotemp.objects.filter(red_flag_temp=True)
    result4 = Kyc_Infotemp.objects.filter(red_flag_temp=False, blue_flag_temp=False, green_flag_temp=False)
    productnames = Kyc_Infotemp.objects.all()

    # get the form output using get method
    if request.method == 'GET':
        p = request.GET.getlist('select_user')
        # print(p)
        # k = request.GET('parameters[]')
        productnames = Kyc_Infotemp.objects.all()
        context = {
            "Kyc_Infotemp1": result, "Kyc_Infotemp2": result2,
            "Kyc_Infotemp3": result3, "Kyc_Infotemp4": result4,
            'userList': p, 'all_info': productnames,
        }

    else:

        context = {
            "Kyc_Infotemp1": result, "Kyc_Infotemp2": result2,
            "Kyc_Infotemp3": result3, "Kyc_Infotemp4": result4,
            "all_info": productnames,
        }
    # passing variables to the update.html using dictionary
    return render(request, "kyc/update.html", context)


# this was defined to check a branch of a program only for devoloping purposes
def productList(request):
    if request.method == 'GET':
        p = request.GET.getlist('select_user')
        print(p)
        # k = request.GET('parameters[]')
        productnames = Kyc_Infotemp.objects.all()
        context = {
            'userList': p, 'all_info': productnames,
        }
        # --- logic later for chart ------

    return render(request, 'kyc/select.html', context)


# defining function to get records using id through the database and display in editing
def edit_val(request, id):
    update_val = Kyc_Infotemp.objects.get(id=id)

    return render(request, "kyc/edit.html", {"Kyc_Infotemp": update_val})


# defining database update function when click on update button
def update_data(request, id):
    if request.method == 'POST' and 'update_db' in request.POST:

        updates_data = Kyc_Infotemp.objects.get(id=id)
        form = update_forms(request.POST, instance=updates_data)

        rejected_temp = request.POST["rejected_temp"]

        if rejected_temp == 'reject_val':

            salutation = request.POST["salutation_temp"]
            full_name = request.POST["full_name_temp"]
            name_init = request.POST["name_init_temp"]
            profile_pic = request.POST["profile_pic_temp"]
            live_video = request.POST["live_video_temp"]
            id_type = request.POST["id_type_temp"]

            try:
                nics_no = request.POST["nics_no_temp"]
                date_of_birth = request.POST["date_of_birth_temp"]
            except MultiValueDictKeyError:
                nics_no = ''
                date_of_birth = ''

            try:
                drive_lic = request.POST.get("driv_lic_temp")
                driv_exp = request.POST["driv_exp_temp"]
            except MultiValueDictKeyError:
                drive_lic = ''
                driv_exp = ''

            try:
                pass_no = request.POST["pass_no_temp"]
                pass_exp = request.POST["pass_exp_temp"]
            except MultiValueDictKeyError:
                pass_no = ''
                pass_exp = ''

            try:
                birth_cernum = request.POST["birth_cernum_temp"]
            except MultiValueDictKeyError:
                birth_cernum = ''

            try:
                post_id = request.POST["post_id_temp"]
            except MultiValueDictKeyError:
                post_id = ''

            try:
                oafsc = request.POST["oafsc_temp"]
            except MultiValueDictKeyError:
                oafsc = ''

            try:
                visa_copy = request.POST["visa_copy_temp"]
            except MultiValueDictKeyError:
                visa_copy = ''

            try:
                othe_identity_doc = request.POST["othe_identity_doc_temp"]
            except MultiValueDictKeyError:
                othe_identity_doc = ''

            nationality = request.POST["nationality_temp"]

            try:
                nationality_other = request.POST["nationality_other_temp"]
                type_of_visa = request.POST["type_of_visa_temp"]
                visa_exp = request.POST["visa_exp_temp"]
                other_types = request.POST["other_types_temp"]
                other_exp = request.POST["other_exp_temp"]
                foreign_addre = request.POST["foreign_addre_temp"]

            except MultiValueDictKeyError:
                nationality_other = ''
                type_of_visa = ''
                visa_exp = ''
                other_types = ''
                other_exp = ''
                foreign_addre = ''

            vari_doc_type = request.POST["vari_doc_type_temp"]
            vari_doc = request.POST["vari_doc_temp"]
            pep_person = request.POST["pep_person_temp"]
            us_city = request.POST["us_city_temp"]

            # calling variables for form inputs in residential detail section
            resident_sri = request.POST["resident_sri_temp"]

            try:
                country_resident = request.POST["country_resident_temp"]
            except MultiValueDictKeyError:
                country_resident = ''

            house_no_per = request.POST["house_no_per_temp"]
            street_per = request.POST["street_per_temp"]
            city_per = request.POST["city_per_temp"]
            postal_code_per = request.POST["postal_code_per_temp"]

            house_no = request.POST["house_no_temp"]
            street = request.POST["street_temp"]
            city = request.POST["city_temp"]
            postal_code = request.POST["postal_code_temp"]
            state_address = request.POST["state_address_temp"]

                    # calling variables for form inputs in contact detail section
            mob_no = request.POST["mob_no_temp"]
            office_num = request.POST["office_num_temp"]
            home_num = request.POST["house_no_temp"]
            email_add = request.POST["email_add_temp"]
            email_add_verification = request.POST["email_add_verification"]

            date_now_temp = request.POST["date_now_temp"]
            staff_member_temp = request.POST["staff_member_temp"]
            file_note_temp = request.POST["file_note_temp"]

            try:
                file_attachment_temp = request.POST["file_attachment_temp"]
            except MultiValueDictKeyError:
                file_attachment_temp = ""
            
            reason_for_rej_temp = request.POST["reason_for_rej_temp"]
            rejected_temp = request.POST["rejected_temp"]
            flag_1 = request.POST["red_flag_temp"]
            flag_2 = request.POST["green_flag_temp"]
            flag_3 = request.POST["blue_flag_temp"]
            masegEmail = "Sorry! \n"
            profile_rating = request.POST["profile_rating_temp"]

            # new form added variables
            post_id_exp_temp = request.POST["post_id_exp_temp"]
            account_type_temp = request.POST["account_type_temp"]
            have_acc_temp = request.POST["have_acc_temp"]
            buisness_trans_temp = request.POST.get("buisness_trans_temp")
            fam_remittance_temp = request.POST.get("fam_remittance_temp")
            prof_income_temp = request.POST.get("prof_income_temp")
            rare_trans_temp = request.POST.get("rare_trans_temp")
            cash_temp = request.POST.get("cash_temp")
            cheque_temp = request.POST.get("cheque_temp")
            std_order_temp = request.POST.get("std_order_temp")
            slip_wir_temp = request.POST.get("slip_wir_temp")
            occu_state_temp = request.POST.get("occu_state_temp")
            occupation_temp = request.POST.get("occupation_temp")
            in_source_sales_temp = request.POST.get("in_source_sales_temp")
            in_source_fam_rem_temp = request.POST.get("in_source_fam_rem_temp")
            in_source_commistion_temp = request.POST.get("in_source_commistion_temp")
            in_source_export_temp = request.POST.get("in_source_export_temp")
            avg_income_temp = request.POST["avg_income_temp"]
            email_varified_temp = request.POST["email_varified_temp"]
            

            submit_kyc_temp = Kyc_Reject(salutation_temp=salutation, full_name_temp=full_name,
                                        name_init_temp=name_init, profile_pic_temp=profile_pic,
                                        live_video_temp=live_video,
                                        id_type_temp=id_type,
                                        nics_no_temp=nics_no, date_of_birth_temp=date_of_birth,
                                        driv_lic_temp=drive_lic, driv_exp_temp=driv_exp,
                                        pass_no_temp=pass_no, pass_exp_temp=pass_exp,
                                        birth_cernum_temp=birth_cernum,
                                        post_id_temp=post_id, oafsc_temp=oafsc, visa_copy_temp=visa_copy,
                                        othe_identity_doc_temp=othe_identity_doc,
                                        nationality_temp=nationality,
                                        nationality_other_temp=nationality_other,
                                        type_of_visa_temp=type_of_visa,
                                        visa_exp_temp=visa_exp, other_types_temp=other_types,
                                        other_exp_temp=other_exp, foreign_addre_temp=foreign_addre,
                                        vari_doc_type_temp=vari_doc_type, vari_doc_temp=vari_doc,
                                        pep_person_temp=pep_person,
                                        us_city_temp=us_city,
                                        resident_sri_temp=resident_sri,
                                        country_resident_temp=country_resident,
                                        house_no_temp=house_no, street_temp=street, city_temp=city,
                                        postal_code_temp=postal_code, state_address_temp=state_address,
                                        house_no_per_temp=house_no_per, street_per_temp=street_per,
                                        city_per_temp=city_per, postal_code_per_temp=postal_code_per,
                                        mob_no_temp=mob_no, office_num_temp=office_num,
                                        home_num_temp=home_num, email_add_verification=email_add_verification,
                                        email_add_temp=email_add, red_flag_temp=flag_1,
                                        green_flag_temp=flag_2, blue_flag_temp=flag_3, date_now_temp=date_now_temp,
                                        staff_member_temp=staff_member_temp, file_note_temp=file_note_temp,
                                        reason_for_rej_temp=reason_for_rej_temp, rejected_temp=rejected_temp,
                                        file_attachment_temp=file_attachment_temp, profile_rating_temp=profile_rating,
                                        post_id_exp_temp=post_id_exp_temp,
                                        account_type_temp=account_type_temp,
                                        have_acc_temp=have_acc_temp,
                                        buisness_trans_temp=buisness_trans_temp,
                                        fam_remittance_temp=fam_remittance_temp,
                                        prof_income_temp=prof_income_temp,
                                        rare_trans_temp=rare_trans_temp,
                                        cash_temp=cash_temp,
                                        cheque_temp=cheque_temp,
                                        std_order_temp=std_order_temp,
                                        slip_wir_temp=slip_wir_temp,
                                        occu_state_temp=occu_state_temp,
                                        occupation_temp=occupation_temp,
                                        in_source_sales_temp=in_source_sales_temp,
                                        in_source_fam_rem_temp=in_source_fam_rem_temp,
                                        in_source_commistion_temp=in_source_commistion_temp,
                                        in_source_export_temp=in_source_export_temp,
                                        avg_income_temp=avg_income_temp,
                                        email_varified_temp=email_varified_temp)

                    
            submit_kyc_temp.save()
            Kyc_Infotemp.objects.filter(id=id).delete()
            messages.success(request, 'successfully submitted')

            
            email_alert("BANK", masegEmail + "Kyc of " + full_name  + "is rejected. on " + date_now_temp + " Please visit the nearest XXX branch or Call xxx-xxxxxxx. Our staff will assist you in this process ", email_add)

            result = Kyc_Infotemp.objects.filter(green_flag_temp=True)
            result2 = Kyc_Infotemp.objects.filter(blue_flag_temp=True)
            result3 = Kyc_Infotemp.objects.filter(red_flag_temp=True)
            result4 = Kyc_Infotemp.objects.filter(red_flag_temp=False, blue_flag_temp=False, green_flag_temp=False)
            productnames = Kyc_Infotemp.objects.all()


            # get the form output using get method
            if request.method == 'GET':
                p = request.GET.getlist('select_user')
                # print(p)
                # k = request.GET('parameters[]')
                productnames = Kyc_Infotemp.objects.all()
                context = {
                    "Kyc_Infotemp1": result, "Kyc_Infotemp2": result2,
                    "Kyc_Infotemp3": result3, "Kyc_Infotemp4": result4,
                    'userList': p, 'all_info': productnames,
                }

            else:

                context = {
                    "Kyc_Infotemp1": result, "Kyc_Infotemp2": result2,
                    "Kyc_Infotemp3": result3, "Kyc_Infotemp4": result4,
                    "all_info": productnames,
                }
            # passing variables to the update.html using dictionary
            return render(request, "kyc/update.html", context)
        
        else:

            updates_data = Kyc_Infotemp.objects.get(id=id)
            form = update_forms(request.POST, instance=updates_data)

            # print(form.errors)

            # print(updates_data)

            print(form.is_valid())

            if form.is_valid():
                form.save()
                messages.warning(request, "record update sucessfully, please select Reject before rejecting")
                return render(request, "kyc/edit.html", {"Kyc_Infotemp": updates_data})

    if request.method == 'POST' and 'accept_rec' in request.POST:

        new_entry = request.POST["nics_no_temp"]
        flag_1 = request.POST["red_flag_temp"]
        flag_2 = request.POST["green_flag_temp"]
        flag_3 = request.POST["blue_flag_temp"]

        masegEmail = "Verification successfull\n"
        full_name = request.POST["full_name_temp"]
        nics_no = request.POST["nics_no_temp"]
        email_add = request.POST["email_add_temp"]

        if Kyc_Info.objects.filter(nics_no_temp=new_entry).exists():

            place = Kyc_Info.objects.get(nics_no_temp=new_entry)
            updates_origin = Kyc_Info.objects.get(id=place.id)

            if (flag_1 == 'False' and flag_2 == 'False' and flag_3 == 'False'):
                form = accept_form(request.POST, instance=updates_origin)

                if form.is_valid():
                    form.save()

                    updates_data = Kyc_Infotemp.objects.get(id=id)
                    form = update_forms(request.POST, instance=updates_data)
                    # Kyc_Infotemp.objects.filter(id=id).delete()
                    Kyc_Infotemp.objects.filter(id=id).delete()

                    email_alert("BANK", masegEmail + "KYC of " + full_name  + " and " + nics_no + " verified successfullly, Thank you for banking with us. ", email_add)

                    result = Kyc_Infotemp.objects.filter(green_flag_temp=True)
                    result2 = Kyc_Infotemp.objects.filter(blue_flag_temp=True)
                    result3 = Kyc_Infotemp.objects.filter(red_flag_temp=True)
                    result4 = Kyc_Infotemp.objects.filter(red_flag_temp=False, blue_flag_temp=False, green_flag_temp=False)
                    productnames = Kyc_Infotemp.objects.all()

                    # get the form output using get method
                    if request.method == 'GET':
                        p = request.GET.getlist('select_user')
                        # print(p)
                        # k = request.GET('parameters[]')
                        productnames = Kyc_Infotemp.objects.all()
                        context = {
                            "Kyc_Infotemp1": result, "Kyc_Infotemp2": result2,
                            "Kyc_Infotemp3": result3, "Kyc_Infotemp4": result4,
                            'userList': p, 'all_info': productnames,
                        }

                    else:

                        context = {
                            "Kyc_Infotemp1": result, "Kyc_Infotemp2": result2,
                            "Kyc_Infotemp3": result3, "Kyc_Infotemp4": result4,
                            "all_info": productnames,
                        }
                    # passing variables to the update.html using dictionary
                    return render(request, "kyc/update.html", context)


            else:
                updates_data = Kyc_Infotemp.objects.get(id=id)
                form = update_forms(request.POST, instance=updates_data)
                messages.error(request, 'please remove flags before adding to main database')
                return render(request, "kyc/edit.html", {"Kyc_Infotemp": updates_data})

            new_entry = request.POST["salutation_temp"]
            print(new_entry)
        # updates_data = Kyc_Infotemp.objects.get(id=id)
        # form = update_forms(request.POST, instance=updates_data)
        # print(form)
        else:

            if (flag_1 == 'False' and flag_2 == 'False' and flag_3 == 'False'):

                salutation = request.POST["salutation_temp"]
                full_name = request.POST["full_name_temp"]
                name_init = request.POST["name_init_temp"]
                profile_pic = request.POST["profile_pic_temp"]
                live_video = request.POST["live_video_temp"]
                id_type = request.POST["id_type_temp"]

                try:
                    nics_no = request.POST["nics_no_temp"]
                    date_of_birth = request.POST["date_of_birth_temp"]
                except MultiValueDictKeyError:
                    nics_no = ''
                    date_of_birth = ''

                try:
                    drive_lic = request.POST.get("driv_lic_temp")
                    driv_exp = request.POST["driv_exp_temp"]
                except MultiValueDictKeyError:
                    drive_lic = ''
                    driv_exp = ''

                try:
                    pass_no = request.POST["pass_no_temp"]
                    pass_exp = request.POST["pass_exp_temp"]
                except MultiValueDictKeyError:
                    pass_no = ''
                    pass_exp = ''

                try:
                    birth_cernum = request.POST["birth_cernum_temp"]
                except MultiValueDictKeyError:
                    birth_cernum = ''

                try:
                    post_id = request.POST["post_id_temp"]
                except MultiValueDictKeyError:
                    post_id = ''

                try:
                    oafsc = request.POST["oafsc_temp"]
                except MultiValueDictKeyError:
                    oafsc = ''

                try:
                    visa_copy = request.POST["visa_copy_temp"]
                except MultiValueDictKeyError:
                    visa_copy = ''

                try:
                    othe_identity_doc = request.POST["othe_identity_doc_temp"]
                except MultiValueDictKeyError:
                    othe_identity_doc = ''

                nationality = request.POST["nationality_temp"]

                try:
                    nationality_other = request.POST["nationality_other_temp"]
                    type_of_visa = request.POST["type_of_visa_temp"]
                    visa_exp = request.POST["visa_exp_temp"]
                    other_types = request.POST["other_types_temp"]
                    other_exp = request.POST["other_exp_temp"]
                    foreign_addre = request.POST["foreign_addre_temp"]

                except MultiValueDictKeyError:
                    nationality_other = ''
                    type_of_visa = ''
                    visa_exp = ''
                    other_types = ''
                    other_exp = ''
                    foreign_addre = ''

                vari_doc_type = request.POST["vari_doc_type_temp"]
                vari_doc = request.POST["vari_doc_temp"]
                pep_person = request.POST["pep_person_temp"]
                us_city = request.POST["us_city_temp"]

                # calling variables for form inputs in residential detail section
                resident_sri = request.POST["resident_sri_temp"]

                try:
                    country_resident = request.POST["country_resident_temp"]
                except MultiValueDictKeyError:
                    country_resident = ''

                house_no_per = request.POST["house_no_per_temp"]
                street_per = request.POST["street_per_temp"]
                city_per = request.POST["city_per_temp"]
                postal_code_per = request.POST["postal_code_per_temp"]

                house_no = request.POST["house_no_temp"]
                street = request.POST["street_temp"]
                city = request.POST["city_temp"]
                postal_code = request.POST["postal_code_temp"]
                state_address = request.POST["state_address_temp"]

                # calling variables for form inputs in contact detail section
                mob_no = request.POST["mob_no_temp"]
                office_num = request.POST["office_num_temp"]
                home_num = request.POST["home_num_temp"]
                email_add = request.POST["email_add_temp"]
                email_add_verification = request.POST["email_add_verification"]
                profile_rating = request.POST["profile_rating_temp"]
                
                # new form added variables
                post_id_exp_temp = request.POST["post_id_exp_temp"]
                account_type_temp = request.POST["account_type_temp"]
                have_acc_temp = request.POST["have_acc_temp"]
                buisness_trans_temp = request.POST.get("buisness_trans_temp")
                fam_remittance_temp = request.POST.get("fam_remittance_temp")
                prof_income_temp = request.POST.get("prof_income_temp")
                rare_trans_temp = request.POST.get("rare_trans_temp")
                cash_temp = request.POST.get("cash_temp")
                cheque_temp = request.POST.get("cheque_temp")
                std_order_temp = request.POST.get("std_order_temp")
                slip_wir_temp = request.POST.get("slip_wir_temp")
                occu_state_temp = request.POST.get("occu_state_temp")
                occupation_temp = request.POST.get("occupation_temp")
                in_source_sales_temp = request.POST.get("in_source_sales_temp")
                in_source_fam_rem_temp = request.POST.get("in_source_fam_rem_temp")
                in_source_commistion_temp = request.POST.get("in_source_commistion_temp")
                in_source_export_temp = request.POST.get("in_source_export_temp")
                avg_income_temp = request.POST["avg_income_temp"]
                email_varified_temp = request.POST["email_varified_temp"]

                submit_kyc_temp = Kyc_Info(salutation_temp=salutation, full_name_temp=full_name,
                                            name_init_temp=name_init, profile_pic_temp=profile_pic,
                                            live_video_temp=live_video,
                                            id_type_temp=id_type,
                                            nics_no_temp=nics_no, date_of_birth_temp=date_of_birth,
                                            driv_lic_temp=drive_lic, driv_exp_temp=driv_exp,
                                            pass_no_temp=pass_no, pass_exp_temp=pass_exp,
                                            birth_cernum_temp=birth_cernum,
                                            post_id_temp=post_id, oafsc_temp=oafsc, visa_copy_temp=visa_copy,
                                            othe_identity_doc_temp=othe_identity_doc,
                                            nationality_temp=nationality,
                                            nationality_other_temp=nationality_other,
                                            type_of_visa_temp=type_of_visa,
                                            visa_exp_temp=visa_exp, other_types_temp=other_types,
                                            other_exp_temp=other_exp, foreign_addre_temp=foreign_addre,
                                            vari_doc_type_temp=vari_doc_type, vari_doc_temp=vari_doc,
                                            pep_person_temp=pep_person,
                                            us_city_temp=us_city,
                                            resident_sri_temp=resident_sri,
                                            country_resident_temp=country_resident,
                                            house_no_temp=house_no, street_temp=street, city_temp=city,
                                            postal_code_temp=postal_code, state_address_temp=state_address,
                                            house_no_per_temp=house_no_per, street_per_temp=street_per,
                                            city_per_temp=city_per, postal_code_per_temp=postal_code_per,
                                            mob_no_temp=mob_no, office_num_temp=office_num,
                                            home_num_temp=home_num, email_add_verification=email_add_verification,
                                            email_add_temp=email_add, red_flag_temp=flag_1,
                                            green_flag_temp=flag_2, blue_flag_temp=flag_3,
                                            profile_rating_temp=profile_rating,
                                            post_id_exp_temp=post_id_exp_temp,
                                            account_type_temp=account_type_temp,
                                            have_acc_temp=have_acc_temp,
                                            buisness_trans_temp=buisness_trans_temp,
                                            fam_remittance_temp=fam_remittance_temp,
                                            prof_income_temp=prof_income_temp,
                                            rare_trans_temp=rare_trans_temp,
                                            cash_temp=cash_temp,
                                            cheque_temp=cheque_temp,
                                            std_order_temp=std_order_temp,
                                            slip_wir_temp=slip_wir_temp,
                                            occu_state_temp=occu_state_temp,
                                            occupation_temp=occupation_temp,
                                            in_source_sales_temp=in_source_sales_temp,
                                            in_source_fam_rem_temp=in_source_fam_rem_temp,
                                            in_source_commistion_temp=in_source_commistion_temp,
                                            in_source_export_temp=in_source_export_temp,
                                            avg_income_temp=avg_income_temp,
                                            email_varified_temp=email_varified_temp
                                            )

                
                submit_kyc_temp.save()
                Kyc_Infotemp.objects.filter(id=id).delete()
                messages.success(request, 'successfully submitted')
                result = Kyc_Infotemp.objects.filter(green_flag_temp=True)
                result2 = Kyc_Infotemp.objects.filter(blue_flag_temp=True)
                result3 = Kyc_Infotemp.objects.filter(red_flag_temp=True)
                result4 = Kyc_Infotemp.objects.filter(red_flag_temp=False, blue_flag_temp=False, green_flag_temp=False)
                productnames = Kyc_Infotemp.objects.all()

                # get the form output using get method
                if request.method == 'GET':
                    p = request.GET.getlist('select_user')
                    # print(p)
                    # k = request.GET('parameters[]')
                    productnames = Kyc_Infotemp.objects.all()
                    context = {
                        "Kyc_Infotemp1": result, "Kyc_Infotemp2": result2,
                        "Kyc_Infotemp3": result3, "Kyc_Infotemp4": result4,
                        'userList': p, 'all_info': productnames,
                    }

                else:

                    context = {
                        "Kyc_Infotemp1": result, "Kyc_Infotemp2": result2,
                        "Kyc_Infotemp3": result3, "Kyc_Infotemp4": result4,
                        "all_info": productnames,
                    }
                # passing variables to the update.html using dictionary
                return render(request, "kyc/update.html", context)

            else:
                updates_data = Kyc_Infotemp.objects.get(id=id)
                form = update_forms(request.POST, instance=updates_data)
                messages.error(request, 'please remove flags before adding to main database')
                return render(request, "kyc/edit.html", {"Kyc_Infotemp": updates_data})



# -----------------------------------------------------------------------------------------------------------------------


# defining method to call accounts page and applying values to the variables
"""def insertkyc1(request):
    # *************variables of second form********************
    global occu_state

    occu_state = request.POST["Occutation_Status"]
    print(occu_state)
    print(full_name)
    print(name_init)

    if Kyc_Info.objects.filter(nics_no=nics_no).exists():
        submit_kyc_temp = Kyc_Infotemp(full_name_temp=full_name, name_init_temp=name_init, id_type_temp=id_type,
                                       nics_no_temp=nics_no, driv_lic_temp=driv_lic,
                                       pass_no_temp=pass_no, nationality_temp=nationality,
                                       nationality_other_temp=nationality_other, house_no_temp=house_no,
                                       street_temp=street,
                                       city_temp=city, mob_no_temp=mob_no, office_num_temp=office_num,
                                       home_num_temp=home_num,
                                       email_add_temp=email_add,
                                       occu_state_temp=occu_state, date_of_birth_temp=date_of_birth,
                                       driv_exp_temp=driv_exp,
                                       green_flag_temp=green_flag, blue_flag_temp=blue_flag, profile_pic=profile_pic)
        submit_kyc_temp.save()
        messages.success(request, 'saved look')
        return render(request, 'kyc/(2nd)AccEmp.html')

    else:

        if Id_Info.objects.filter(nic_no=nics_no, name_full=full_name, birth_day=date_of_birth,
                                  house_num=house_no,
                                  street_add=street, city_ref=city).exists():

            submit_kyc = Kyc_Info(full_name=full_name, name_init=name_init, id_type=id_type, nics_no=nics_no,
                                  driv_lic=driv_lic,
                                  pass_no=pass_no, nationality=nationality,
                                  nationality_other=nationality_other, house_no=house_no, street=street,
                                  city=city, mob_no=mob_no, office_num=office_num, home_num=home_num,
                                  email_add=email_add,
                                  occu_state=occu_state, date_of_birth=date_of_birth, driv_exp=driv_exp, profile_pic=profile_pic)
            submit_kyc.save()
            messages.success(request, 'Successfully saved')

            return render(request, 'kyc/(2nd)AccEmp.html')
        else:

            submit_kyc_temp = Kyc_Infotemp(full_name_temp=full_name, name_init_temp=name_init, id_type_temp=id_type,
                                           nics_no_temp=nics_no, driv_lic_temp=driv_lic,
                                           pass_no_temp=pass_no, nationality_temp=nationality,
                                           nationality_other_temp=nationality_other, house_no_temp=house_no,
                                           street_temp=street,
                                           city_temp=city, mob_no_temp=mob_no, office_num_temp=office_num,
                                           home_num_temp=home_num,
                                           email_add_temp=email_add,
                                           occu_state_temp=occu_state, date_of_birth_temp=date_of_birth,
                                           driv_exp_temp=driv_exp, red_flag_temp=red_flag,
                                           green_flag_temp=green_flag, blue_flag_temp=blue_flag)
            submit_kyc_temp.save()
            messages.success(request, 'saved look')
            return render(request, 'kyc/(2nd)AccEmp.html')"""
# def verify(request):


def insertkyc(request, data_set):
    print("successfully completed")


    # definging global variables
    # -----------------------------------------------------------------------------------------------------------------------

    # ***************** variables of personal information first form ***************

    global salutation, full_name, name_init, profile_pic, id_type, nics_no, date_of_birth, drive_lic, driv_exp, pass_no, pass_exp
    global birth_cernum, post_id, oafsc, visa_copy, othe_identity_doc, nationality, nationality_other, type_of_visa, visa_exp
    global other_types, other_exp, foreign_addre, vari_doc_type, vari_doc, pep_person, us_city, profile_rating

    # global full_name_temp, name_init_temp, date_of_birth_temp

    # variables of residential details
    global resident_sri, country_resident, house_no, street, city, postal_code, state_address, house_no_per, street_per
    global city_per, postal_code_per

    # variables of contact information
    global mob_no, office_num, home_num, email_add, email_varified_temp

    global post_id_exp_temp, account_type_temp, have_acc_temp, buisness_trans_temp, fam_remittance_temp, prof_income_temp
    global rare_trans_temp, cash_temp, cheque_temp, std_order_temp, slip_wir_temp, occu_state_temp, occupation_temp
    global in_source_sales_temp, in_source_fam_rem_temp, in_source_commistion_temp, in_source_export_temp, avg_income_temp

    # variable for flags
    global green_flag, blue_flag, red_flag, saved_id_for_email_vari
    green_flag = False
    blue_flag = False
    red_flag = False
    email_varified_temp= False

    # calling variables for form inputs in personal detail section
    salutation = data_set.salutation_temp
    full_name = data_set.full_name_temp
    name_init = data_set.name_init_temp
    profile_pic = data_set.profile_pic_temp
    live_video = data_set.live_video_temp
    id_type = data_set.id_type_temp
    nics_no = data_set.nics_no_temp
    date_of_birth = data_set.date_of_birth_temp
    drive_lic = data_set.driv_lic_temp
    driv_exp = data_set.driv_exp_temp
    pass_no = data_set.pass_no_temp
    pass_exp = data_set.pass_exp_temp
    birth_cernum =data_set.birth_cernum_temp
    post_id = data_set.post_id_temp
    oafsc = data_set.oafsc_temp


    visa_copy = data_set.visa_copy_temp
    othe_identity_doc = data_set.othe_identity_doc_temp
    nationality = data_set.nationality_temp
    nationality_other = data_set.nationality_other_temp
    type_of_visa = data_set.type_of_visa_temp
    visa_exp = data_set.visa_exp_temp
    other_types = data_set.other_types_temp
    other_exp = data_set.other_exp_temp
    foreign_addre = data_set.foreign_addre_temp


    vari_doc_type = data_set.vari_doc_type_temp
    vari_doc = data_set.vari_doc_temp
    pep_person = data_set.pep_person_temp
    us_city = data_set.us_city_temp

    # calling variables for form inputs in residential detail section

    resident_sri = data_set.resident_sri_temp
    country_resident = data_set.country_resident_temp
    house_no_per = data_set.house_no_per_temp
    street_per = data_set.street_per_temp
    city_per = data_set.city_per_temp

    postal_code_per = data_set.postal_code_per_temp
    house_no = data_set.house_no_temp
    street = data_set.street_temp
    city = data_set.city_temp
    postal_code = data_set.postal_code_temp
    state_address = data_set.state_address_temp
    # calling variables for form inputs in contact detail section

    mob_no = data_set.mob_no_temp
    office_num = data_set.office_num_temp
    home_num = data_set.home_num_temp
    email_add = data_set.email_add_temp

    email_add_verification=round(100000*random.random())
    masegEmail = "you submit kyc information success\n"
    codeEmail = str(email_add_verification)

    # profile rating
    profile_rating = 'evaluate later'
    post_id_exp_temp = data_set.post_id_exp_temp
    account_type_temp = data_set.account_type_temp
    have_acc_temp = data_set.have_acc_temp
    buisness_trans_temp = data_set.buisness_trans_temp
    fam_remittance_temp = data_set.fam_remittance_temp
    prof_income_temp = data_set.prof_income_temp
    rare_trans_temp = data_set.rare_trans_temp
    cash_temp = data_set.cash_temp
    cheque_temp = data_set.cheque_temp
    std_order_temp = data_set.std_order_temp
    slip_wir_temp = data_set.slip_wir_temp
    occu_state_temp = data_set.occu_state_temp
    occupation_temp = data_set.occupation_temp
    in_source_sales_temp = data_set.in_source_sales_temp
    in_source_fam_rem_temp = data_set.in_source_fam_rem_temp
    in_source_commistion_temp = data_set.in_source_commistion_temp
    in_source_export_temp = data_set.in_source_export_temp
    avg_income_temp = data_set.avg_income_temp

    rightFlag = []
    wrongFlag = []
    rightFlag2 = []
    wrongFlag2 = []

    chekCity = 0
    chekname = 0
    chekhome = 0
    chekStreet = 0



# checking is there ID exists in Identity information database
    if Id_Info.objects.filter(nic_no=nics_no).exists():
        rightFlag.insert(len(rightFlag) + 1, "nic no ok")
    else:
        wrongFlag.insert(len(wrongFlag) + 1, "nic no wrong")

    # check if birthday is true according to id info database
    if Id_Info.objects.filter(nic_no=nics_no, birth_day=date_of_birth).exists():
        rightFlag.insert(len(rightFlag) + 1, "birthday is ok")
    else:
        wrongFlag.insert(len(wrongFlag) + 1, "birthday is wrong")

    if len(rightFlag) > 1:

        # if true for existing kyc
        # messages.success(request, 'existing kyc')

        if Kyc_Infotemp.objects.filter(nics_no_temp=nics_no).exists():
            sub_form = Kyc_Infotemp.objects.filter(nics_no_temp=nics_no).count()
            
        else:
            sub_form = 0

        messages.success(request, rightFlag)
        # check whether the full name is similar to id info database
        if Id_Info.objects.filter(nic_no=nics_no, name_full=full_name).exists():
            rightFlag2.insert(len(rightFlag2) + 1, "name is ok")
        else:
            wrongFlag2.insert(len(wrongFlag2) + 1, "name is wrong")
            chekname = 1

        if Id_Info.objects.filter(nic_no=nics_no, house_num=house_no, ).exists():
            rightFlag2.insert(len(rightFlag2) + 1, "house number is ok")
        else:
            wrongFlag2.insert(len(wrongFlag2) + 1, "house number is wrong")
            chekhome = 1

        if Id_Info.objects.filter(nic_no=nics_no, city_ref=city).exists():
            rightFlag2.insert(len(rightFlag2) + 1, "city is ok")
        else:
            wrongFlag2.insert(len(wrongFlag2) + 1, "city is wrong")
            chekCity = 1

        if Id_Info.objects.filter(nic_no=nics_no, street_add=street).exists():
            rightFlag2.insert(len(rightFlag2) + 1, "street address is ok")
        else:
            wrongFlag2.insert(len(wrongFlag2) + 1, "street address is wrong")
            chekStreet = 1


        if len(rightFlag2) > 3:
            green_flag = False
            blue_flag = False
            red_flag = False

            submit_kyc_temp = Kyc_Infotemp(salutation_temp=salutation, full_name_temp=full_name,
                                           name_init_temp=name_init, profile_pic_temp=profile_pic,
                                           live_video_temp=live_video,
                                           id_type_temp=id_type,
                                           nics_no_temp=nics_no, date_of_birth_temp=date_of_birth,
                                           driv_lic_temp=drive_lic, driv_exp_temp=driv_exp,
                                           pass_no_temp=pass_no, pass_exp_temp=pass_exp,
                                           birth_cernum_temp=birth_cernum,
                                           post_id_temp=post_id, oafsc_temp=oafsc, visa_copy_temp=visa_copy,
                                           othe_identity_doc_temp=othe_identity_doc,
                                           nationality_temp=nationality,
                                           nationality_other_temp=nationality_other,
                                           type_of_visa_temp=type_of_visa,
                                           visa_exp_temp=visa_exp, other_types_temp=other_types,
                                           other_exp_temp=other_exp, foreign_addre_temp=foreign_addre,
                                           vari_doc_type_temp=vari_doc_type, vari_doc_temp=vari_doc,
                                           pep_person_temp=pep_person,
                                           us_city_temp=us_city,
                                           resident_sri_temp=resident_sri,
                                           country_resident_temp=country_resident,
                                           house_no_temp=house_no, street_temp=street, city_temp=city,
                                           postal_code_temp=postal_code, state_address_temp=state_address,
                                           house_no_per_temp=house_no_per, street_per_temp=street_per,
                                           city_per_temp=city_per, postal_code_per_temp=postal_code_per,
                                           mob_no_temp=mob_no, office_num_temp=office_num,
                                           home_num_temp=home_num,
                                           email_add_temp=email_add,
                                           email_add_verification=email_add_verification, red_flag_temp=red_flag, 
                                           green_flag_temp=green_flag, blue_flag_temp=blue_flag,
                                           submited_form=sub_form,
                                           check_city=chekCity,
                                           check_name=chekname,
                                           check_home=chekhome,
                                           check_street=chekStreet,
                                           profile_rating_temp=profile_rating,
                                           post_id_exp_temp =post_id_exp_temp,
                                           account_type_temp =account_type_temp,
                                           have_acc_temp =have_acc_temp,
                                           buisness_trans_temp =buisness_trans_temp,
                                           fam_remittance_temp =fam_remittance_temp,
                                           prof_income_temp =prof_income_temp,
                                           rare_trans_temp =rare_trans_temp,
                                           cash_temp =cash_temp,
                                           cheque_temp =cheque_temp,
                                           std_order_temp =std_order_temp,
                                           slip_wir_temp =slip_wir_temp,
                                           occu_state_temp =occu_state_temp,
                                           occupation_temp =occupation_temp,
                                           in_source_sales_temp =in_source_sales_temp,
                                           in_source_fam_rem_temp =in_source_fam_rem_temp,
                                           in_source_commistion_temp =in_source_commistion_temp,
                                           in_source_export_temp =in_source_export_temp,
                                           avg_income_temp =avg_income_temp,
                                           email_varified_temp=email_varified_temp)
            submit_kyc_temp.save()
            # messages.success(request, rightFlag2)
            idS = str(submit_kyc_temp.id)
            saved_id_for_email_vari = submit_kyc_temp.id
            # request.session['id'] = submit_kyc_temp.id
            email_alert("BANK", masegEmail + "http://127.0.0.1:8000/verify?ecode=" + codeEmail + "&id=" + idS,
                        email_add)
            #return render(request, 'kyc/verify.html')
            data_set.delete()
            return None

        else:
            if len(rightFlag2) > 2:
                green_flag = True
            else:
                if len(rightFlag2) > 1:
                    blue_flag = True
                else:
                    red_flag = True

            submit_kyc_temp = Kyc_Infotemp(salutation_temp=salutation, full_name_temp=full_name,
                                name_init_temp=name_init, profile_pic_temp=profile_pic,
                                live_video_temp=live_video,
                                id_type_temp=id_type,
                                nics_no_temp=nics_no, date_of_birth_temp=date_of_birth,
                                driv_lic_temp=drive_lic, driv_exp_temp=driv_exp,
                                pass_no_temp=pass_no, pass_exp_temp=pass_exp,
                                birth_cernum_temp=birth_cernum,
                                post_id_temp=post_id, oafsc_temp=oafsc, visa_copy_temp=visa_copy,
                                othe_identity_doc_temp=othe_identity_doc,
                                nationality_temp=nationality,
                                nationality_other_temp=nationality_other,
                                type_of_visa_temp=type_of_visa,
                                visa_exp_temp=visa_exp, other_types_temp=other_types,
                                other_exp_temp=other_exp, foreign_addre_temp=foreign_addre,
                                vari_doc_type_temp=vari_doc_type, vari_doc_temp=vari_doc,
                                pep_person_temp=pep_person,
                                us_city_temp=us_city,
                                resident_sri_temp=resident_sri,
                                country_resident_temp=country_resident,
                                house_no_temp=house_no, street_temp=street, city_temp=city,
                                postal_code_temp=postal_code, state_address_temp=state_address,
                                house_no_per_temp=house_no_per, street_per_temp=street_per,
                                city_per_temp=city_per, postal_code_per_temp=postal_code_per,
                                mob_no_temp=mob_no, office_num_temp=office_num,
                                home_num_temp=home_num,
                                email_add_temp=email_add,
                                email_add_verification=email_add_verification, red_flag_temp=red_flag,
                                green_flag_temp=green_flag, blue_flag_temp=blue_flag, submited_form=sub_form,
                                check_city=chekCity,
                                check_name=chekname,
                                check_home=chekhome,
                                check_street=chekStreet,profile_rating_temp=profile_rating,
                                post_id_exp_temp = post_id_exp_temp,
                                account_type_temp = account_type_temp,
                                have_acc_temp = have_acc_temp,
                                buisness_trans_temp = buisness_trans_temp,
                                fam_remittance_temp = fam_remittance_temp,
                                prof_income_temp = prof_income_temp,
                                rare_trans_temp = rare_trans_temp,
                                cash_temp = cash_temp,
                                cheque_temp = cheque_temp,
                                std_order_temp = std_order_temp,
                                slip_wir_temp = slip_wir_temp,
                                occu_state_temp = occu_state_temp,
                                occupation_temp = occupation_temp,
                                in_source_sales_temp = in_source_sales_temp,
                                in_source_fam_rem_temp = in_source_fam_rem_temp,
                                in_source_commistion_temp = in_source_commistion_temp,
                                in_source_export_temp = in_source_export_temp,
                                avg_income_temp = avg_income_temp,
                                email_varified_temp=email_varified_temp)
            submit_kyc_temp.save()
            print(len(rightFlag))
            idS = str(submit_kyc_temp.id)
            saved_id_for_email_vari = submit_kyc_temp.id
            # request.session['id'] = submit_kyc_temp.id
            email_alert("BANK", masegEmail + "http://127.0.0.1:8000/verify?ecode=" + codeEmail + "&id=" + idS,
                        email_add)
            # return render(request, 'kyc/verify.html')
            data_set.delete()
            return None


    else:
        messages.warning(request, wrongFlag)
        #return render(request, 'kyc/index.html')
        return None



    # # checking is there ID exists in Identity information database
    # if Id_Info.objects.filter(nic_no=nics_no).exists():

    #     # if exists id number proceed to next step
    #     #messages.success(request, 'NIC validated successfully')

    #     # check whether there are existing kyc in the database to the given id number
    #     if Kyc_Infotemp.objects.filter(nics_no_temp=nics_no).exists():

    #         # if true for existing kyc
    #         # messages.success(request, 'existing kyc')

    #         # check whether the full name is similar to id info database
    #         if Id_Info.objects.filter(nic_no=nics_no, name_full=full_name).exists():

    #             # return to next page
    #             # return render(request, 'kyc/(2nd)AccEmp.html')

    #             # give an message if name is true
    #             # messages.success(request, 'existing kyc, name true')

    #             # check if birthday is true according to id info database
    #             if Id_Info.objects.filter(nic_no=nics_no, name_full=full_name, birth_day=date_of_birth).exists():

    #                 # giving a message if dob is true
    #                 # messages.success(request, 'existing kyc, name true,dob ture')

    #                 if Id_Info.objects.filter(nic_no=nics_no, name_full=full_name, birth_day=date_of_birth,
    #                                           house_num=house_no,
    #                                           street_add=street, city_ref=city).exists():
    #                     green_flag = 'True'

    #                     #messages.success(request, 'existing kyc, name true, dob ture, address true')

    #                     submit_kyc_temp = Kyc_Infotemp(salutation_temp=salutation, full_name_temp=full_name,
    #                                                    name_init_temp=name_init, profile_pic_temp=profile_pic,
    #                                                    live_video_temp=live_video,
    #                                                    id_type_temp=id_type,
    #                                                    nics_no_temp=nics_no, date_of_birth_temp=date_of_birth,
    #                                                    driv_lic_temp=drive_lic, driv_exp_temp=driv_exp,
    #                                                    pass_no_temp=pass_no, pass_exp_temp=pass_exp,
    #                                                    birth_cernum_temp=birth_cernum,
    #                                                    post_id_temp=post_id, oafsc_temp=oafsc, visa_copy_temp=visa_copy,
    #                                                    othe_identity_doc_temp=othe_identity_doc,
    #                                                    nationality_temp=nationality,
    #                                                    nationality_other_temp=nationality_other,
    #                                                    type_of_visa_temp=type_of_visa,
    #                                                    visa_exp_temp=visa_exp, other_types_temp=other_types,
    #                                                    other_exp_temp=other_exp, foreign_addre_temp=foreign_addre,
    #                                                    vari_doc_type_temp=vari_doc_type, vari_doc_temp=vari_doc,
    #                                                    pep_person_temp=pep_person,
    #                                                    us_city_temp=us_city,
    #                                                    resident_sri_temp=resident_sri,
    #                                                    country_resident_temp=country_resident,
    #                                                    house_no_temp=house_no, street_temp=street, city_temp=city,
    #                                                    postal_code_temp=postal_code, state_address_temp=state_address,
    #                                                    house_no_per_temp=house_no_per, street_per_temp=street_per,
    #                                                    city_per_temp=city_per, postal_code_per_temp=postal_code_per,
    #                                                    mob_no_temp=mob_no, office_num_temp=office_num,
    #                                                    home_num_temp=home_num,
    #                                                    email_add_temp=email_add,
    #                                                    email_add_verification=email_add_verification, red_flag_temp=red_flag,
    #                                                    green_flag_temp=green_flag, blue_flag_temp=blue_flag, 
    #                                                    profile_rating_temp=profile_rating)
    #                     submit_kyc_temp.save()
    #                     messages.success(request, 'Your submission is recorded. We will contact you soon!')
    #                     idS =  str(submit_kyc_temp.id)
    #                     request.session['id'] = submit_kyc_temp.id

    #                     email_alert("BANK", masegEmail + "http://127.0.0.1:8000/verify?ecode=" + codeEmail + "&id=" + idS, email_add)

    #                     return render(request, 'kyc/verify.html')
    #                     print(green_flag)

    #                 else:

    #                     """messages.warning(request, 'existing kyc, name true,dob true, address false attach proof '
    #                                               'document')"""

    #                     blue_flag = 'True'
    #                     submit_kyc_temp = Kyc_Infotemp(salutation_temp=salutation, full_name_temp=full_name,
    #                                                    name_init_temp=name_init, profile_pic_temp=profile_pic,
    #                                                    live_video_temp=live_video,
    #                                                    id_type_temp=id_type,
    #                                                    nics_no_temp=nics_no, date_of_birth_temp=date_of_birth,
    #                                                    driv_lic_temp=drive_lic, driv_exp_temp=driv_exp,
    #                                                    pass_no_temp=pass_no, pass_exp_temp=pass_exp,
    #                                                    birth_cernum_temp=birth_cernum,
    #                                                    post_id_temp=post_id, oafsc_temp=oafsc, visa_copy_temp=visa_copy,
    #                                                    othe_identity_doc_temp=othe_identity_doc,
    #                                                    nationality_temp=nationality,
    #                                                    nationality_other_temp=nationality_other,
    #                                                    type_of_visa_temp=type_of_visa,
    #                                                    visa_exp_temp=visa_exp, other_types_temp=other_types,
    #                                                    other_exp_temp=other_exp, foreign_addre_temp=foreign_addre,
    #                                                    vari_doc_type_temp=vari_doc_type, vari_doc_temp=vari_doc,
    #                                                    pep_person_temp=pep_person,
    #                                                    us_city_temp=us_city,
    #                                                    resident_sri_temp=resident_sri,
    #                                                    country_resident_temp=country_resident,
    #                                                    house_no_temp=house_no, street_temp=street, city_temp=city,
    #                                                    postal_code_temp=postal_code, state_address_temp=state_address,
    #                                                    house_no_per_temp=house_no_per, street_per_temp=street_per,
    #                                                    city_per_temp=city_per, postal_code_per_temp=postal_code_per,
    #                                                    mob_no_temp=mob_no, office_num_temp=office_num,
    #                                                    home_num_temp=home_num,
    #                                                    email_add_temp=email_add,
    #                                                    email_add_verification=email_add_verification, red_flag_temp=red_flag,
    #                                                    green_flag_temp=green_flag, blue_flag_temp=blue_flag,
    #                                                    profile_rating_temp=profile_rating)
    #                     submit_kyc_temp.save()
    #                     messages.success(request, 'Your submission is recorded. We will contact you soon!')
    #                     idS =  str(submit_kyc_temp.id)
    #                     request.session['id'] = submit_kyc_temp.id

    #                     email_alert("BANK", masegEmail + "http://127.0.0.1:8000/verify?ecode=" + codeEmail + "&id=" + idS, email_add)

    #                     return render(request, 'kyc/verify.html')

    #             # if date of birth is false
    #             else:
    #                 # give an error message
    #                 messages.error(request, 'Date of birth is invalid, please check again')
    #                 return render(request, 'kyc/verify.html')
    #         else:
    #             # give an message if name is false
    #             messages.error(request, 'Invalid name, please check again')
    #             return render(request, 'kyc/verify.html')

    #     else:

    #         print(drive_lic)
    #         print(driv_exp)
    #         print(id_type)
    #         print(nics_no)
    #         print(date_of_birth)
    #         # print(driv_exp)

    #         # check whether the full name is similar to id info database
    #         if Id_Info.objects.filter(nic_no=nics_no, name_full=full_name).exists():

    #             # return to next page
    #             # return render(request, 'kyc/(2nd)AccEmp.html')

    #             # give an message if name is true
    #             # messages.success(request, 'no kyc, name true')

    #             # check if birthday is true according to id info database
    #             if Id_Info.objects.filter(nic_no=nics_no, name_full=full_name, birth_day=date_of_birth).exists():

    #                 # giving a message if dob is true
    #                 # messages.success(request, 'no kyc, name true,dob ture')

    #                 if Id_Info.objects.filter(nic_no=nics_no, name_full=full_name, birth_day=date_of_birth,
    #                                           house_num=house_no,
    #                                           street_add=street, city_ref=city).exists():

    #                     #messages.success(request, 'no kyc, name true, dob ture, address true')

    #                     submit_kyc_temp = Kyc_Infotemp(salutation_temp=salutation, full_name_temp=full_name,
    #                                                    name_init_temp=name_init, profile_pic_temp=profile_pic,
    #                                                    live_video_temp=live_video,
    #                                                    id_type_temp=id_type,
    #                                                    nics_no_temp=nics_no, date_of_birth_temp=date_of_birth,
    #                                                    driv_lic_temp=drive_lic, driv_exp_temp=driv_exp,
    #                                                    pass_no_temp=pass_no, pass_exp_temp=pass_exp,
    #                                                    birth_cernum_temp=birth_cernum,
    #                                                    post_id_temp=post_id, oafsc_temp=oafsc, visa_copy_temp=visa_copy,
    #                                                    othe_identity_doc_temp=othe_identity_doc,
    #                                                    nationality_temp=nationality,
    #                                                    nationality_other_temp=nationality_other,
    #                                                    type_of_visa_temp=type_of_visa,
    #                                                    visa_exp_temp=visa_exp, other_types_temp=other_types,
    #                                                    other_exp_temp=other_exp, foreign_addre_temp=foreign_addre,
    #                                                    vari_doc_type_temp=vari_doc_type, vari_doc_temp=vari_doc,
    #                                                    pep_person_temp=pep_person,
    #                                                    us_city_temp=us_city,
    #                                                    resident_sri_temp=resident_sri,
    #                                                    country_resident_temp=country_resident,
    #                                                    house_no_temp=house_no, street_temp=street, city_temp=city,
    #                                                    postal_code_temp=postal_code, state_address_temp=state_address,
    #                                                    house_no_per_temp=house_no_per, street_per_temp=street_per,
    #                                                    city_per_temp=city_per, postal_code_per_temp=postal_code_per,
    #                                                    mob_no_temp=mob_no, office_num_temp=office_num,
    #                                                    home_num_temp=home_num,
    #                                                    email_add_temp=email_add,
    #                                                    email_add_verification=email_add_verification, red_flag_temp=red_flag,
    #                                                    green_flag_temp=green_flag, blue_flag_temp=blue_flag,
    #                                                    profile_rating_temp=profile_rating)
    #                     submit_kyc_temp.save()
    #                     messages.success(request, 'Your submission is recorded. We will contact you soon!')
    #                     idS =  str(submit_kyc_temp.id)
    #                     request.session['id'] = submit_kyc_temp.id

    #                     email_alert("BANK", masegEmail + "http://127.0.0.1:8000/verify?ecode=" + codeEmail + "&id=" + idS, email_add)

    #                     return render(request, 'kyc/verify.html')

    #                 else:

    #                     """messages.warning(request, 'no kyc, name true,dob true, address false attach proof '
    #                                               'document')"""

    #                     red_flag = True

    #                     submit_kyc_temp = Kyc_Infotemp(salutation_temp=salutation, full_name_temp=full_name,
    #                                                    name_init_temp=name_init, profile_pic_temp=profile_pic,
    #                                                    live_video_temp=live_video,
    #                                                    id_type_temp=id_type,
    #                                                    nics_no_temp=nics_no, date_of_birth_temp=date_of_birth,
    #                                                    driv_lic_temp=drive_lic, driv_exp_temp=driv_exp,
    #                                                    pass_no_temp=pass_no, pass_exp_temp=pass_exp,
    #                                                    birth_cernum_temp=birth_cernum,
    #                                                    post_id_temp=post_id, oafsc_temp=oafsc, visa_copy_temp=visa_copy,
    #                                                    othe_identity_doc_temp=othe_identity_doc,
    #                                                    nationality_temp=nationality,
    #                                                    nationality_other_temp=nationality_other,
    #                                                    type_of_visa_temp=type_of_visa,
    #                                                    visa_exp_temp=visa_exp, other_types_temp=other_types,
    #                                                    other_exp_temp=other_exp, foreign_addre_temp=foreign_addre,
    #                                                    vari_doc_type_temp=vari_doc_type, vari_doc_temp=vari_doc,
    #                                                    pep_person_temp=pep_person,
    #                                                    us_city_temp=us_city,
    #                                                    resident_sri_temp=resident_sri,
    #                                                    country_resident_temp=country_resident,
    #                                                    house_no_temp=house_no, street_temp=street, city_temp=city,
    #                                                    postal_code_temp=postal_code, state_address_temp=state_address,
    #                                                    house_no_per_temp=house_no_per, street_per_temp=street_per,
    #                                                    city_per_temp=city_per, postal_code_per_temp=postal_code_per,
    #                                                    mob_no_temp=mob_no, office_num_temp=office_num,
    #                                                    home_num_temp=home_num,
    #                                                    email_add_temp=email_add,
    #                                                    email_add_verification=email_add_verification, red_flag_temp=red_flag,
    #                                                    green_flag_temp=green_flag, blue_flag_temp=blue_flag,
    #                                                    profile_rating_temp=profile_rating)
    #                     submit_kyc_temp.save()
    #                     messages.success(request, 'Your submission is recorded. We will contact you soon!')

    #                     idS =  str(submit_kyc_temp.id)
    #                     request.session['id'] = submit_kyc_temp.id

    #                     email_alert("BANK", masegEmail + "http://127.0.0.1:8000/verify?ecode=" + codeEmail + "&id=" + idS, email_add)

    #                     return render(request, 'kyc/verify.html')




    #             # If date of birth is false
    #             else:
    #                 # give an error message
    #                 messages.warning(request, 'Invalid date of birth, please check again')
    #                 return render(request, 'kyc/verify.html')
    #         else:
    #             # give an message if name is false
    #             messages.error(request, 'Invalid name, please check again')
    #             return render(request, 'kyc/index.html')

    #         # messages.success(request, 'Successfully submitted')
    #         # return to next page
    #         # return render(request, 'kyc/(2nd)AccEmp.html')
    #         # return render(request, 'kyc/index.html')

    # # it there is no id number in id information system give error message
    # else:

    #     messages.error(request, 'Invalid NIC Number. please check again')
    #     return render(request, 'kyc/verify.html')

    """if request.method=='POST':
        if request.POST.get('ID_type'):
            savekyc = Kyc_info()
            savekyc = request.POST.get('ID_type')
            savekyc.save()
            messages.success(request, 'successful')
            return render(request, 'kyc/index.html')

    else:
        return render(request, 'kyc/index.html')"""

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'kyc/home.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'kyc/home.html', {'form': form})


def search_val(request):
    if request.method == "POST":
        nic_no = request.POST["nics_no_temp"]

        if Kyc_Info.objects.filter(nics_no_temp=nic_no).exists():

            # create a global record to contain record id of the nic thats given
            global record_id_nic_search, record_nic_search
            
            # importing searched record wtih all the values and find the id
            find_record = Kyc_Info.objects.get(nics_no_temp=nic_no)
            record_id_nic_search = find_record.id
            record_nic_search =find_record.nics_no_temp
            print(record_id_nic_search)

            return render(request, 'exist_cus/otp.html')
        else:
            messages.success(request, 'Please fill the above details')
            return render(request, 'kyc/index1.html')

    return render(request, 'kyc/search.html')

"""def search_val(request):
    if request.method == "POST":
        nic_no = request.POST["nics_no_temp"]

        if Kyc_Info.objects.filter(nics_no_temp=nic_no).exists():
            messages.success(request, 'Successfully load your data')

            
            finded_user = Kyc_Info.objects.get(nics_no_temp=nic_no)
            form = accept_form(request.POST, instance=finded_user)


            #print(finded_user)
            #print(form.errors)
            if form.is_valid():
                print(form.is_valid())
                form.save()
            
            
            
            context = {
                "Kyc_Infotemp": finded_user,
            }


            return render(request, 'kyc/search.html', context)
        else:
            messages.success(request, 'Please fill the above details')
            return render(request, 'kyc/index1.html')

    return render(request, 'kyc/search.html')"""

def update_main(request):
    return render(request, "kyc/update_main.html")




def reject(request):
    result = Kyc_Reject.objects.filter(green_flag_temp=True)
    result2 = Kyc_Reject.objects.filter(blue_flag_temp=True)
    result3 = Kyc_Reject.objects.filter(red_flag_temp=True)
    result4 = Kyc_Reject.objects.filter(red_flag_temp=False, blue_flag_temp=False, green_flag_temp=False)
    productnames = Kyc_Reject.objects.all()

    # get the form output using get method
    if request.method == 'GET':
        p = request.GET.getlist('select_user')
        # print(p)
        # k = request.GET('parameters[]')
        productnames = Kyc_Reject.objects.all()
        context = {
            "Kyc_Reject1": result, "Kyc_Reject2": result2,
            "Kyc_Reject3": result3, "Kyc_Reject4": result4,
            'userList': p, 'Kyc_Reject': productnames,
        }

    else:

        context = {
            "Kyc_Reject1": result, "Kyc_Reject2": result2,
            "Kyc_Reject3": result3, "Kyc_Reject4": result4,
            "Kyc_Reject": productnames,
        }
    # passing variables to the update.html using dictionary
    return render(request, "kyc/reject.html", context)

def edit_val1(request, id):
    update_val = Kyc_Reject.objects.get(id=id)

    return render(request, "kyc/edit_reject.html", {"Kyc_Reject": update_val})



def update_history(request):
    
    history_user = HistoricalKyc_Info.objects.all()
    

    # get the form output using get method
    if request.method == 'GET':
        
        searched_nic = request.GET.getlist('idval')
        search_filter = request.GET.getlist('select_user')
        # print(p)
        # k = request.GET('parameters[]')
        history_user = HistoricalKyc_Info.objects.all()
        both_user = zip(history_user, searched_nic,search_filter)
        filter_and_search = zip(searched_nic,search_filter)
        context = {
            
            'all_info': history_user, 'ziped': both_user,
            'searched_nic': filter_and_search, 'search_fileter': search_filter,
        }

    else:

        context = {
            
            "all_info": history_user,
        }
    # passing variables to the update.html using dictionary
    return render(request, "kyc/update_history.html", context)

#================================================================New customer form managemetn=================================================

# creating method for new customer data grabbig in front page which is index1.html.

def front(request):

    # creating global variable to grab the id of the saving record
    global grab_id

    if request.method == 'POST':
        # grabbing data form the index1.html 
        salutation = request.POST["salutation"]
        full_name = request.POST["fullname"]
        mob_no = request.POST["mobile_number"]
        office_num = request.POST["office_number"]
        home_num = request.POST["home_number"]
        email_add = request.POST["email_add"]
        

        submit_val= Kyc_front(salutation_temp=salutation, full_name_temp=full_name, mob_no_temp=mob_no,
                                office_num_temp=office_num, home_num_temp=home_num, email_add_temp=email_add)
        
        submit_val.save()
        grab_id = str(submit_val.id)
        print(grab_id)
            
        
        return render(request, "new_cus/new_costomer_form2.html")

    else:

        return render(request, "kyc/index1.html")


def new_cus_form2(request):

    if request.POST.get("nics_no_temp") != "":
        
        # taking the values of the new customer form 2 template
        nics_no_temp = request.POST.get("nics_no_temp")
        date_of_birth_temp = request.POST.get("date_of_birth_temp")
        id_type_temp = request.POST.get("id_type_temp")
        driv_lic_temp = request.POST.get("driv_lic_temp")
        driv_exp_temp = request.POST.get("driv_exp_temp")
        pass_no_temp = request.POST.get("pass_no_temp")
        pass_exp_temp = request.POST.get("pass_exp_temp")
        post_id_temp = request.POST.get("post_id_temp")
        post_id_exp_temp = request.POST.get("post_id_exp_temp")
        birth_cernum_temp = request.POST.get("birth_cernum_temp")
        oafsc_temp = request.POST.get("oafsc_temp")
        othe_identity_doc_temp = request.FILES["othe_identity_doc_temp"]

        # updating objects of the kyc_front where id = grab_id
        Kyc_front.objects.filter(id=grab_id).update(nics_no_temp=nics_no_temp, date_of_birth_temp=date_of_birth_temp, id_type_temp=id_type_temp,
        driv_lic_temp=driv_lic_temp, driv_exp_temp=driv_exp_temp, pass_no_temp=pass_no_temp, pass_exp_temp=pass_exp_temp, post_id_temp=post_id_temp, 
        post_id_exp_temp=post_id_exp_temp, birth_cernum_temp=birth_cernum_temp, oafsc_temp=oafsc_temp)

        # this code is used to save the file to the database
        adding_vari_doc = Kyc_front.objects.get(id=grab_id)
        adding_vari_doc.othe_identity_doc_temp = othe_identity_doc_temp
        adding_vari_doc.save()
        
        print(nics_no_temp)
        return render(request, "new_cus/new_customer3.html")
    else:
        return render(request, "new_cus/new_costomer_form2.html")


def new_cus_form3(request):
    if request.POST.get("house_no_temp") != "":

        resident_sri_temp = request.POST.get("resident_sri_temp")
        country_resident_temp = request.POST.get("country_resident_temp")
        house_no_temp = request.POST.get("house_no_temp")
        street_temp = request.POST.get("street_temp")
        city_temp = request.POST.get("city_temp")
        postal_code_temp = request.POST.get("postal_code_temp")
        house_no_per_temp = request.POST.get("house_no_per_temp")
        street_per_temp = request.POST.get("street_per_temp")
        city_per_temp = request.POST.get("city_per_temp")
        postal_code_per_temp = request.POST.get("postal_code_per_temp")
        state_address_temp = request.POST.get("state_address_temp")
        vari_doc_temp = request.FILES["vari_doc_temp"]
        

        Kyc_front.objects.filter(id=grab_id).update(resident_sri_temp=resident_sri_temp, country_resident_temp=country_resident_temp,
        house_no_temp=house_no_temp, street_temp=street_temp, city_temp=city_temp, postal_code_temp=postal_code_temp,
        house_no_per_temp=house_no_per_temp, street_per_temp=street_per_temp, city_per_temp=city_per_temp, postal_code_per_temp=postal_code_per_temp,
        state_address_temp=state_address_temp)

        # address varification documetn adding to kyc_front db
        address_veri_doc = Kyc_front.objects.get(id=grab_id)
        address_veri_doc.vari_doc_temp = vari_doc_temp
        address_veri_doc.save()
        
        print(house_no_temp)
        return render(request, "new_cus/new_costomer_form4.html")
    else:
        return render(request,"new_cus/new_customer3.html")

def new_cus_form4(request):
    if request.POST.get("nationality_temp") != "default":

        nationality_temp = request.POST.get("nationality_temp")
        nationality_other_temp = request.POST.get("nationality_other_temp")
        type_of_visa_temp = request.POST.get("type_of_visa_temp")
        visa_exp_temp = request.POST.get("visa_exp_temp")
        other_types_temp = request.POST.get("other_types_temp")
        other_exp_temp = request.POST.get("other_exp_temp")
        try:
            visa_copy_temp = request.FILES["visa_copy_temp"]
        except MultiValueDictKeyError:
            visa_copy_temp = ''
        
        
        Kyc_front.objects.filter(id=grab_id).update(nationality_temp=nationality_temp, nationality_other_temp=nationality_other_temp,
        type_of_visa_temp=type_of_visa_temp, visa_exp_temp=visa_exp_temp, other_types_temp=other_types_temp,
        other_exp_temp=other_exp_temp)

        insert_visa_copy = Kyc_front.objects.get(id=grab_id)
        insert_visa_copy.visa_copy_temp = visa_copy_temp
        insert_visa_copy.save()
        
        print(nationality_temp)
        return render(request, "new_cus/new_costomer_form5.html")
    else:
        return render(request,"new_cus/new_costomer_form4.html")

def new_cus_form5(request):
    if request.POST.get("profile_pic_temp") != "":

        profile_pic_temp = request.FILES["profile_pic_temp"]
        live_video_temp = request.FILES["live_video_temp"]
        
        insert_image = Kyc_front.objects.get(id=grab_id)
        insert_image.profile_pic_temp = profile_pic_temp
        insert_image.live_video_temp = live_video_temp
        insert_image.save()

        print(profile_pic_temp)
        return render(request, "new_cus/new_costomer_form6.html")
    else:
        return render(request,"new_cus/new_costomer_form5.html")

def new_cus_form6(request):
    if request.POST.get("account_type_temp") != "":

        account_type_temp = request.POST.get("account_type_temp")
        have_acc_temp = request.POST.get("have_acc_temp")
        buisness_trans_temp = request.POST.get("buisness_trans_temp")
        fam_remittance_temp = request.POST.get("fam_remittance_temp")
        prof_income_temp = request.POST.get("prof_income_temp")
        rare_trans_temp = request.POST.get("rare_trans_temp")
        cash_temp = request.POST.get("cash_temp")
        cheque_temp = request.POST.get("cheque_temp")
        std_order_temp = request.POST.get("std_order_temp")
        slip_wir_temp = request.POST.get("slip_wir_temp")

        print(have_acc_temp, buisness_trans_temp, fam_remittance_temp, prof_income_temp, rare_trans_temp,
        cash_temp, cheque_temp, std_order_temp, slip_wir_temp)

        Kyc_front.objects.filter(id=grab_id).update(account_type_temp=account_type_temp, have_acc_temp=have_acc_temp,
        buisness_trans_temp=buisness_trans_temp, fam_remittance_temp=fam_remittance_temp, cash_temp=cash_temp, 
        prof_income_temp=prof_income_temp, rare_trans_temp=rare_trans_temp, cheque_temp=cheque_temp, 
        std_order_temp=std_order_temp, slip_wir_temp=slip_wir_temp)
        
        print(account_type_temp)
        return render(request, "new_cus/new_customer_7.html")
    else:
        return render(request,"new_cus/new_costomer_form6.html")

def new_cus_form7(request):
    if request.POST.get("occu_state_temp") != "":

        occu_state_temp = request.POST.get("occu_state_temp")
        pep_person_temp = request.POST.get("pep_person_temp")
        occupation_temp = request.POST.get("occupation_temp")
        in_source_sales_temp = request.POST.get("in_source_sales_temp")
        in_source_fam_rem_temp = request.POST.get("in_source_fam_rem_temp")
        in_source_commistion_temp = request.POST.get("in_source_commistion_temp")
        in_source_export_temp = request.POST.get("in_source_export_temp")
        avg_income_temp = request.POST.get("avg_income_temp")
        


        Kyc_front.objects.filter(id=grab_id).update(occu_state_temp=occu_state_temp, occupation_temp=occupation_temp,
        in_source_sales_temp=in_source_sales_temp, in_source_fam_rem_temp=in_source_fam_rem_temp,
        in_source_commistion_temp=in_source_commistion_temp, in_source_export_temp=in_source_export_temp,
        avg_income_temp=avg_income_temp, pep_person_temp=pep_person_temp)

        data_set = Kyc_front.objects.get(id=grab_id)
        insertkyc(request, data_set)
        
        
        print(occu_state_temp)
        return render(request, "kyc/verify.html")

    else:
        return render(request,"new_cus/new_customer_7.html")

# ====================end of new customer form management===================================================================================

#============================================================ existing customer management ==================================================
global system_gen_otp, system_gen_otp_new

def exist_cus_otp(request):

    # defining global variable to system_gen otp

    if request.method == 'POST' and 'Next' in request.POST:

        # initializing otp 
        system_gen_otp = 1000

        if request.POST.get("enterd_otp") == str(system_gen_otp):
            print("otp next")
            print(record_id_nic_search, record_nic_search)

            return render(request, "exist_cus/welcome.html")

        else:

            print("invalid otp")
            return render(request, "exist_cus/otp.html")

        
    elif request.method == 'POST' and 'Resend' in request.POST:
        print("otp resend")

    elif request.method == 'POST' and 'Back' in request.POST:
        print("redircting to root")
        return render(request, 'kyc/search.html')


    return render(request, "exist_cus/otp.html")


def exist_cus_update_info(request):

    if request.method == 'POST' and 'No_need_change' in request.POST:
        return render(request, "kyc/search.html")

    return render(request, "exist_cus/updateinfo.html")

def exist_cus_form(request):

    finded_user = Kyc_Info.objects.get(nics_no_temp=record_nic_search)
    # form = accept_form(request.POST, instance=finded_user)

    # create id to pass in to the defined function
    funtion_id = finded_user.id

    print(finded_user.email_add_temp)

    if request.method == 'POST' and 'update_new' in request.POST:

        # section one dataset
        salutation_temp = request.POST.get('salutation_temp')   #0
        full_name_temp = request.POST.get('full_name_temp')     #1
        mob_no_temp = request.POST.get('mob_no_temp')           #2
        email_add_temp = request.POST.get('email_add_temp')     #3
        home_num_temp = request.POST.get('home_num_temp')       #4
        office_num_temp = request.POST.get('office_num_temp')   #5
        
        # section two dataset
        nics_no_temp = request.POST.get("nics_no_temp")                 #6
        date_of_birth_temp = request.POST.get("date_of_birth_temp")     #7
        id_type_temp = request.POST.get("id_type_temp")                 #8
        driv_lic_temp = request.POST.get("driv_lic_temp")               #9
        driv_exp_temp = request.POST.get("driv_exp_temp")               #10
        pass_no_temp = request.POST.get("pass_no_temp")                 #11
        pass_exp_temp = request.POST.get("pass_exp_temp")               #12
        post_id_temp = request.POST.get("post_id_temp")                 #13
        post_id_exp_temp = request.POST.get("post_id_exp_temp")         #14
        birth_cernum_temp = request.POST.get("birth_cernum_temp")       #15
        oafsc_temp = request.POST.get("oafsc_temp")                     #16

        try:
            othe_identity_doc_temp = request.FILES["othe_identity_doc_temp"]    #17
        except:
            othe_identity_doc_temp = ""
        # section 3 dataset

        resident_sri_temp = request.POST.get("resident_sri_temp")               #18
        country_resident_temp = request.POST.get("country_resident_temp")       #19
        house_no_temp = request.POST.get("house_no_temp")                       #20
        street_temp = request.POST.get("street_temp")                           #21
        city_temp = request.POST.get("city_temp")                               #22
        postal_code_temp = request.POST.get("postal_code_temp")                 #23
        house_no_per_temp = request.POST.get("house_no_per_temp")               #24 
        street_per_temp = request.POST.get("street_per_temp")                   #25
        city_per_temp = request.POST.get("city_per_temp")                       #26
        postal_code_per_temp = request.POST.get("postal_code_per_temp")         #27
        state_address_temp = request.POST.get("state_address_temp")             #28
        try:    
            vari_doc_temp = request.FILES["vari_doc_temp"]                      #29
        except:
            vari_doc_temp = ""
        # section 4 dataset

        nationality_temp = request.POST.get("nationality_temp")                 #30
        nationality_other_temp = request.POST.get("nationality_other_temp")     #31
        type_of_visa_temp = request.POST.get("type_of_visa_temp")               #32
        visa_exp_temp = request.POST.get("visa_exp_temp")                       #33
        other_types_temp = request.POST.get("other_types_temp")                 #34
        other_exp_temp = request.POST.get("other_exp_temp")                     #35
        try:
            visa_copy_temp = request.FILES["visa_copy_temp"]                    #36
        except MultiValueDictKeyError:
            visa_copy_temp = ''

        # section 5 dataset
        try:
            profile_pic_temp = request.FILES["profile_pic_temp"]                #37
        except:
            profile_pic_temp = "" 

        try:
            live_video_temp = request.FILES["live_video_temp"]                  #38
        except:
            live_video_temp = ""

        # section 6 dataset
        account_type_temp = request.POST.get("account_type_temp")       #39
        have_acc_temp = request.POST.get("have_acc_temp")               #40
        buisness_trans_temp = request.POST.get("buisness_trans_temp")   #41
        fam_remittance_temp = request.POST.get("fam_remittance_temp")   #42
        prof_income_temp = request.POST.get("prof_income_temp")         #43
        rare_trans_temp = request.POST.get("rare_trans_temp")           #44
        cash_temp = request.POST.get("cash_temp")                       #45
        cheque_temp = request.POST.get("cheque_temp")                   #46
        std_order_temp = request.POST.get("std_order_temp")             #47
        slip_wir_temp = request.POST.get("slip_wir_temp")               #48

        #section 7 dataset
        occu_state_temp = request.POST.get("occu_state_temp")                   #49
        pep_person_temp = request.POST.get("pep_person_temp")                   #50
        occupation_temp = request.POST.get("occupation_temp")                   #51
        in_source_sales_temp = request.POST.get("in_source_sales_temp")         #52
        in_source_fam_rem_temp = request.POST.get("in_source_fam_rem_temp")     #53
        in_source_commistion_temp = request.POST.get("in_source_commistion_temp")   #54
        in_source_export_temp = request.POST.get("in_source_export_temp")           #55
        avg_income_temp = request.POST.get("avg_income_temp")                       #56

        data_list_to_save = np.array([salutation_temp, full_name_temp, mob_no_temp, email_add_temp, home_num_temp, office_num_temp,
                                    nics_no_temp, date_of_birth_temp, id_type_temp, driv_lic_temp, driv_exp_temp, pass_no_temp, pass_exp_temp,
                                    post_id_temp, post_id_exp_temp, birth_cernum_temp, oafsc_temp, othe_identity_doc_temp,
                                    resident_sri_temp, country_resident_temp, house_no_temp, street_temp, city_temp,
                                    postal_code_temp,
                                    house_no_per_temp,
                                    street_per_temp,
                                    city_per_temp,
                                    postal_code_per_temp,
                                    state_address_temp,
                                    vari_doc_temp,
                                    nationality_temp,
                                    nationality_other_temp,
                                    type_of_visa_temp,
                                    visa_exp_temp,
                                    other_types_temp,
                                    other_exp_temp,
                                    visa_copy_temp,
                                    profile_pic_temp,
                                    live_video_temp,
                                    account_type_temp,
                                    have_acc_temp,
                                    buisness_trans_temp,
                                    fam_remittance_temp,
                                    prof_income_temp,
                                    rare_trans_temp,
                                    cash_temp,
                                    cheque_temp,
                                    std_order_temp,
                                    slip_wir_temp,
                                    occu_state_temp,
                                    pep_person_temp,
                                    occupation_temp,
                                    in_source_sales_temp,
                                    in_source_fam_rem_temp,
                                    in_source_commistion_temp,
                                    in_source_export_temp,
                                    avg_income_temp])

        make_save_list(request, funtion_id, data_list_to_save)

        finded_user = Kyc_Info.objects.get(nics_no_temp=record_nic_search)

        context = {
            "Kyc_Infotemp": finded_user,
        }

        return render(request, "exist_cus/existing_customer.html", context)
        
    
    
    context = {
        "Kyc_Infotemp": finded_user,
    }

    return render(request, "exist_cus/existing_customer.html", context)

# end of existing customer management

def make_save_list(request, function_id, dataset_list_for_func):
    great = dataset_list_for_func

    id_set = function_id

    print(great)
    #print(great)

    # section one dataset======================================================================================

    # salutation_temp = great[0]
    # full_name_temp = great[1]
    # mob_no_temp = great[2]
    # email_add_temp =great[3]

    home_num_temp = great[4]
    office_num_temp = great[5]
    Kyc_Info.objects.filter(id=function_id).update(home_num_temp=home_num_temp, office_num_temp=office_num_temp)

    # section two dataset=======================================================================================

    # nics_no_temp = great[6]
    date_of_birth_temp = great[7]
    id_type_temp = great[8]
    driv_lic_temp = great[9]
    driv_exp_temp = great[10]
    pass_no_temp = great[11]
    pass_exp_temp = great[12]
    post_id_temp = great[13]
    post_id_exp_temp = great[14]
    birth_cernum_temp = great[15]
    oafsc_temp = great[16]
    othe_identity_doc_temp = great[17]

    Kyc_Info.objects.filter(id=function_id).update(date_of_birth_temp=date_of_birth_temp, id_type_temp=id_type_temp,
        driv_lic_temp=driv_lic_temp, driv_exp_temp=driv_exp_temp, pass_no_temp=pass_no_temp, pass_exp_temp=pass_exp_temp, 
        post_id_temp=post_id_temp, post_id_exp_temp=post_id_exp_temp, birth_cernum_temp=birth_cernum_temp, oafsc_temp=oafsc_temp)

    # defingig a variable to insert files to sepcific location of the qurary set
    insert_image_quary = Kyc_Info.objects.get(id=function_id)

    if othe_identity_doc_temp != "":
        insert_image_quary.othe_identity_doc_temp = othe_identity_doc_temp
        insert_image_quary.save()

    # section 3 dataset==============================================================================================

    resident_sri_temp = great[18]
    country_resident_temp = great[19]
    house_no_temp = great[20]
    street_temp = great[21]
    city_temp = great[22]
    postal_code_temp = great[23]
    # house_no_per_temp = great[24]
    # street_per_temp = great[25]
    # city_per_temp = great[26]
    # postal_code_per_temp = great[27]
    state_address_temp = great[28]
    vari_doc_temp = great[29]
    
    Kyc_Info.objects.filter(id=function_id).update(resident_sri_temp=resident_sri_temp, country_resident_temp=country_resident_temp,
        house_no_temp=house_no_temp, street_temp=street_temp, city_temp=city_temp, postal_code_temp=postal_code_temp,
        state_address_temp=state_address_temp)

    if vari_doc_temp != "":
        insert_image_quary.vari_doc_temp = vari_doc_temp
        insert_image_quary.save()

    # section 4 dataset================================================================================================

    nationality_temp = great[30]
    nationality_other_temp = great[31]
    type_of_visa_temp = great[32]
    visa_exp_temp = great[33]
    other_types_temp = great[34]
    other_exp_temp = great[35]
    visa_copy_temp = great[36]

    Kyc_Info.objects.filter(id=function_id).update(nationality_temp=nationality_temp, nationality_other_temp=nationality_other_temp,
        type_of_visa_temp=type_of_visa_temp, visa_exp_temp=visa_exp_temp, other_types_temp=other_types_temp,
        other_exp_temp=other_exp_temp)

    if visa_copy_temp != "":
        insert_image_quary.visa_copy_temp = visa_copy_temp
        insert_image_quary.save()


    # section 5 dataset================================================================================================================


    profile_pic_temp = great[37]
    live_video_temp = great[38]

    if profile_pic_temp != "":
        insert_image_quary.profile_pic_temp = profile_pic_temp
        insert_image_quary.save()

    if live_video_temp != "":
        insert_image_quary.live_video_temp = live_video_temp
        insert_image_quary.save()

    # section 6 dataset==============================================================================================


    account_type_temp = great[39]
    have_acc_temp = great[40]
    buisness_trans_temp = great[41]
    fam_remittance_temp = great[42]
    prof_income_temp = great[43]
    rare_trans_temp = great[44]
    cash_temp = great[45]
    cheque_temp = great[46]
    std_order_temp = great[47]
    slip_wir_temp = great[48]

    Kyc_Info.objects.filter(id=function_id).update(account_type_temp=account_type_temp, have_acc_temp=have_acc_temp,
        buisness_trans_temp=buisness_trans_temp, fam_remittance_temp=fam_remittance_temp, cash_temp=cash_temp, 
        prof_income_temp=prof_income_temp, rare_trans_temp=rare_trans_temp, cheque_temp=cheque_temp, 
        std_order_temp=std_order_temp, slip_wir_temp=slip_wir_temp)


    #section 7 dataset============================================================================================

    
    occu_state_temp = great[49]
    pep_person_temp = great[50]
    occupation_temp = great[51]
    in_source_sales_temp = great[52]
    in_source_fam_rem_temp = great[53]
    in_source_commistion_temp = great[54]
    in_source_export_temp = great[55]
    avg_income_temp = great[56]

    Kyc_Info.objects.filter(id=function_id).update(occu_state_temp=occu_state_temp, occupation_temp=occupation_temp,
        in_source_sales_temp=in_source_sales_temp, in_source_fam_rem_temp=in_source_fam_rem_temp,
        in_source_commistion_temp=in_source_commistion_temp, in_source_export_temp=in_source_export_temp,
        avg_income_temp=avg_income_temp, pep_person_temp=pep_person_temp)


    
    return None


def social_score(request):

    if request.method == 'POST':

        # personal details
        edu_qualifi = request.POST.get("edu_qualifi")
        emp_details = request.POST.get("emp_details")
        spent_hours_video = request.POST.get("spent_hours_video")
        job_status = request.POST.get("job_status")

        # relations details
        relations_name = request.POST.get("relations_name")
        relations_address = request.POST.get("relations_address")
        rel_relationship = request.POST.get("rel_relationship")
        rel_job_type = request.POST.get("rel_job_type")
        rel_job_status = request.POST.get("rel_job_status")

        #friends details
        friend_name = request.POST.get("friend_name")
        friend_address = request.POST.get("friend_address")
        friend_job_type = request.POST.get("friend_job_type")
        friend_job_status = request.POST.get("friend_job_status")
        
        # volunteer services
        volun_service = request.POST.get("volun_service")

        # sergery deails
        ser_heart = request.POST.get("ser_heart")
        ser_cancer = request.POST.get("ser_cancer")
        ser_kidney = request.POST.get("ser_kidney")
        ser_none = request.POST.get("ser_none")
        ser_other = request.POST.get("ser_other")

        # major disease details
        dis_diabetics = request.POST.get("dis_diabetics")
        dis_cholestrol = request.POST.get("dis_cholestrol")
        dis_blood_presure = request.POST.get("dis_blood_presure")
        dis_none = request.POST.get("dis_none")
        dis_other = request.POST.get("dis_other")

        # passing variable sto social score model table
        scoial_score_record = Social_core(edu_qualifi=edu_qualifi, emp_details=emp_details, spent_hours_video=spent_hours_video,
         job_status=job_status, relations_name=relations_name, relations_address=relations_address,
        rel_relationship= rel_relationship, rel_job_type=rel_job_type, rel_job_status=rel_job_status,
        friend_name=friend_name, friend_address=friend_address, friend_job_type=friend_job_type, friend_job_status=friend_job_status,
        volun_service=volun_service, 
        ser_heart=ser_heart, ser_cancer=ser_cancer, ser_kidney=ser_kidney, ser_none=ser_none, ser_other=ser_other,
        dis_diabetics=dis_diabetics, dis_cholestrol=dis_cholestrol, dis_blood_presure=dis_blood_presure, dis_none=dis_none,
        dis_other=dis_other)

        scoial_score_record.save()

        
    return render(request, 'social_score/Social_score.html')