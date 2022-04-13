import streamlit as st
import datetime
import jpholiday


def is_national_holiday(dt_date):
    return jpholiday.is_holiday(dt_date)


def is_sun_or_sat(dt_date):
    if dt_date.weekday() == 5 or dt_date.weekday() == 6:
        return True
    else:
        return False


def is_nenmatu(dt_date):
    today_str = dt_date.strftime('%m%d')
    nemmatsu = ['1229', '1230', '1231', '0101', '0102', '0103']
    if today_str in nemmatsu:
        return True
    else:
        return False


def is_business_day(dt_date):
    if is_national_holiday(dt_date) or is_sun_or_sat(dt_date) or is_nenmatu(dt_date):
        return False
    else:
        return True


def cal_futaku_date(lead_days, target_date_dt):
    bussinessdays_arr = []
    unit_day = datetime.timedelta(days=1)
    while len(bussinessdays_arr) != lead_days:
        target_date_dt = target_date_dt - unit_day
        if is_business_day(target_date_dt):
            bussinessdays_arr.append(target_date_dt)
        else:
            continue
    return bussinessdays_arr[-1]


def cal_futaku_date2(lead_days, target_date2_dt):
    bussinessdays_arr = []
    unit_day = datetime.timedelta(days=1)

    while len(bussinessdays_arr) < lead_days:
        target_date2_dt = target_date2_dt + unit_day
        if is_business_day(target_date2_dt):
             bussinessdays_arr.append(target_date2_dt)
        else:
            continue

    return bussinessdays_arr[-1]

def total_business_days(today_dt, target_day_dt):
    date = today_dt
    counter = 0
    while date < target_day_dt:
        unit_day = datetime.timedelta(days=1)
        date = date + unit_day

        if is_business_day(date):
            counter += 1
        else:
            continue

    return counter

def ret_date_prop(target_date2):
    target_date2_dt = datetime.datetime.strptime(target_date2, '%Y%m%d')

    date_prop = '国民の祝日、または土日、年末年始に該当していません'

    if jpholiday.is_holiday_name(target_date2_dt):
        date_prop = jpholiday.is_holiday_name(target_date2_dt) + 'になっています。'

    elif is_sun_or_sat(target_date2_dt):
        date_prop = '土日になっています！！'

    elif is_nenmatu(target_date2_dt):
        date_prop = '年末年始になっています！！'

    return date_prop

def main():
    st.title('営業日カウンター Produced by KJ')
    '-------------------------------------------------------------------------------------'
    yosan = st.selectbox('予算規模を選択してください！', ['1億以下', '1億超過5億以下', '5億超過'])
    if yosan == '1億以下':
        lead_days = 30
    if yosan == '1億超過5億以下':
        lead_days = 40
    if yosan == '5億超過':
        lead_days = 45
    'リードタイム：', lead_days, '営業日必要'
    '--------------------------------------------------------------------------------------'
    today_dt = datetime.datetime.today()
    today_str= datetime.datetime.strftime(today_dt, '%Y%m%d')



    target_date2 = st.text_input(
        'ターゲット日を指定しそこから工期初日を割り出す場合：　　(↓yyyymmdd形式で工期初日を指定)', value=today_str)
    target_date2_dt = datetime.datetime.strptime(target_date2, '%Y%m%d')
    kouki_date2 = cal_futaku_date2(lead_days, target_date2_dt)
    target_date2_str = datetime.datetime.strftime(target_date2_dt, '%Y年%m月%d日')
    kouki_date2_str = datetime.datetime.strftime(kouki_date2, '%Y年%m月%d日')
    date_prop =  ret_date_prop(target_date2)

    '指定日は：　　', date_prop
    '付託の日：　　', target_date2_str
    '工期初日：　　', kouki_date2_str, '　　以降が推奨されます。'
    '--------------------------------------------------------------------------------------'
    ##来年度4月1日を初期値に指定##
    month_today = today_dt.month
    year_today = today_dt.year

    if 4 <= month_today <= 12:
        next_year = datetime.date(year=year_today + 1, month=4, day=1)
    else:
        next_year = datetime.date(year=year_today, month=4, day=1)
    next_year_str = datetime.datetime.strftime(next_year, '%Y%m%d')
    #################
    target_date = st.text_input(
        '工期初日から付託期日を算出する場合：　　(↓yyyymmdd形式で工期初日を指定)', value=next_year_str)
    target_date_dt = datetime.datetime.strptime(target_date, '%Y%m%d')

    futaku_date = cal_futaku_date(lead_days, target_date_dt)
    futaku_date_str = datetime.datetime.strftime(futaku_date, '%Y年%m月%d日')
    target_date_str = datetime.datetime.strftime(target_date_dt, '%Y年%m月%d日')
    counter = total_business_days(today_dt, target_date_dt)
    date_prop0 =  ret_date_prop(target_date)

    '指定日は：　　', date_prop0
    '工期初日：　　', target_date_str, '　　まで', counter, '営業日'
    '請負付託：　　', futaku_date_str, '　　までの実施が推奨されます。'
    '--------------------------------------------------------------------------------------'


if __name__ == '__main__':
    main()
