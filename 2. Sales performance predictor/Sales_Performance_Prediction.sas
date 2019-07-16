/*IMPORTING TRANSPOSED 2013 STORE METRICS DATA*/
PROC IMPORT DATAFILE='C:\Users\sxm180029\Desktop\DSC\SM13_upd.xlsx' OUT =SM13 DBMS=xlsx replace;                             
RUN;                                                                                                                                    
                                                                                                                                        
 /*IMPORTING TRANSPOSED 2014 DATA*/                                                                                                                                                                                                                                                                                                                                                                                            
PROC IMPORT DATAFILE='C:\Users\sxm180029\Desktop\DSC\SM14_upd.xlsx' OUT =SM14 DBMS=xlsx replace;                          
RUN;        

/*IMPORTING STORE CHARACTERISTICS DATA*/                                                                                                                                     
PROC IMPORT DATAFILE='C:\Users\sxm180029\Desktop\DSC\Store_charateristics_vf_UP.csv' OUT =SC DBMS=CSV replace;                          
RUN; 
  
/*IMPORTING FOOTTRAFFIC DATA*/                                                                                                                                        
PROC IMPORT DATAFILE='C:\Users\sxm180029\Desktop\DSC\Store_footTraffic_upd.csv' OUT =SFT DBMS=CSV replace; 
RUN;  

/*MERGING STORE METRICS, CHARACTERISTICS AND FOOTTRAFFIC DATA*/
data SFT;
   rename Plant=store_id
          FISCAL_YEAR_PERIOD=TS_ID;
   set sft;
run;

data SC;
   rename Plant=store_id;
   set sc;
run;

data  SF;
   merge SM13 
         SM14
         SFT;
   by  Store_ID TS_ID;
run;

data  SSF;
   merge SF
         SC;
   by  Store_ID;
run;

/* EXPORTING DATA TO CSV AND USED PYTHON TO IMPUTE MISSING VALUES FOR STORE METRIC VARIABLES*/
proc export data=SSF
   outfile='C:\Users\sxm180029\Desktop\DSC\SSF_logistic.csv'
   dbms=csv
   replace;
run;

/*IMPORTING MERGED DATA WITH IMPUTED VALUES FOR MISSING STORE METRICS*/
PROC IMPORT DATAFILE='C:\Users\sxm180029\Desktop\DSC\SSF_logisticup.csv' OUT =SSF_logs DBMS=CSV replace;                          
RUN; 

/* CREATING DUMMY AND BINARY VARIABLES*/
data SSF_logso;
set SSF_logs;
if Store_Type='Rel' then store_type_RL=1; else store_type_RL=0;
if Store_Type='Rem' then store_type_RM=1; else store_type_RM=0;
if Store_Type='' then store_type_RL=.;
if Store_Type='' then store_type_RM=.;
if Trade_Area_Size='Large Market' then TAS_Large=1; else TAS_Large=0;
if Trade_Area_Size='Medium Market' then TAS_Med=1; else TAS_Med=0;
if Trade_Area_Size='' then TAS_Large=.;
if Trade_Area_Size='' then TAS_Med=.;
if Does_Store_Have_a_Fleet_Delivery='Y' then Fleet_Del=1; else Fleet_Del=0;
if Does_Store_Have_a_Fleet_Delivery='' then Fleet_Del=.;
if Store_Size='Group 2 > $2.75M' then SS_ge2_75=1; else SS_ge2_75=0;
if Store_Size='Group 3 > $10M' then SS_ge10=1; else SS_ge10=0;
if Store_Size='' then SS_ge2_75=.;
if Store_Size='' then SS_ge10=.;
if Monthly_SMA_MTD___to_Quota<1 then SMA=0; else SMA=1;
if Monthly_SMA_MTD___to_Quota=. then SMA=.;
if Monthly_Store_Account_MTD___to_Q<1 then Store_acc=0; else Store_acc=1;
if Monthly_Store_Account_MTD___to_Q=. then Store_acc=.;
if Monthly_WC_MTD___to_Quota<1 then WC=0; else WC=1;
if Monthly_WC_MTD___to_Quota=. then WC=.;
if Monthly_Parts___Supplies_MTD___t<1 then PnS=0; else PnS=1;
if Monthly_Parts___Supplies_MTD___t=. then PnS=.;
run;

/*IMPORTING ZIP DEMOGRAPHICS*/
PROC IMPORT DATAFILE='C:\Users\sxm180029\Desktop\DSC\ZIP_LND_WTR.csv' OUT =Zip_LW DBMS=CSV replace;                          
RUN; 

/* MERGING DATA WITH ZIP DEMOGRAPHICS*/
data Zip_LW;
set Zip_LW;
rename Zip_Key=Store_Zip;
run;

proc sort data=SSF_logso;
by Store_Zip;
run;

proc sort data=Zip_LW;
by Store_Zip;
run;

data SSF_logson;
merge SSF_logso (IN=aa)
      Zip_LW;
	  if aa;
by Store_Zip;
run;

proc sort data=SSF_logson;
by store_id TS_ID;
run;

/*FINDING STORES WITH ZERO RECORDS FOR EVERY TIME ID*/
proc sql;
select store_id,count(ts_id) from SSF_logson group by store_id;
quit;

/*DELETING RECORD FOR NO RECORDS FOR A PARTICULAR TIME ID*/
proc sql;
delete from  SSF_logson where store_id='A2AC';
quit;


/* TRYING DIFFERENT INTERACTION TERMS*/
data SSF_logson;
set SSF_logson;
ft_mcalls=Monthly_Phonecalls*foottraffic;
ss_ft=SS_ge2_75*foottraffic;
ft_avgtkt=foottraffic*Monthly_Avg_Tkt_Rev;
ft_yoy=footraffic*Monthly_Avg_Tkt_YoY_Growth;
water_ft=WATERSQMI*foottraffic;
run;
/*From the results of the interaction tests, we did not find any of the interaction terms as significant at 95%*/

/*taking log for foottraffic data*/
data SSF_logson;
set SSF_logson;
lnft=log(foottraffic);
run;


/*MODEL 1*/
/* LOGISTIC REGRESIION*/
proc logistic data=SSF_logson  descending;
class store_id ts_id;
model WC= SMA Store_acc Fleet_Del store_type_RL store_type_RM TAS_Large TAS_Med SS_ge2_75 SS_ge10 Monthly_VOC Monthly_Phonecalls Monthly_Mktg_Adopt
                       Monthly_Avg_Tkt_YoY_Growth Monthly_Avg_Tkt_Rev_PnS Monthly_Avg_Tkt_Rev WATERSQMI LANDSQMI HSGUNITS foottraffic Population;
run; 


/*Comments on the model: this model cannot be used as it is not accounting for within store effects since the data we have is a panel data*/

/*MODEL 2*/
/* STRATA OPTION with logigistic regression*/
proc logistic data=SSF_logson  descending;
strata store_id ;
model WC= SMA Store_acc Fleet_Del store_type_RL store_type_RM TAS_Large TAS_Med SS_ge2_75 SS_ge10 Monthly_VOC Monthly_Phonecalls Monthly_Mktg_Adopt
                       Monthly_Avg_Tkt_YoY_Growth Monthly_Avg_Tkt_Rev_PnS Monthly_Avg_Tkt_Rev WATERSQMI LANDSQMI HSGUNITS foottraffic Population;
run; 
/* comment on model: this model does not account for time invariant factors,only considers fixed effects*/


/*MODEL 3*/
/*GENMOD*/
proc genmod data=SSF_logson descend;
class store_id ts_id/order=formatted;;
model WC(descending)= SMA  Store_acc Fleet_Del store_type_RL store_type_RM TAS_Large TAS_Med SS_ge2_75 SS_ge10 Monthly_VOC Monthly_Phonecalls Monthly_Mktg_Adopt
                       Monthly_Avg_Tkt_YoY_Growth Monthly_Avg_Tkt_Rev_PnS Monthly_Avg_Tkt_Rev WATERSQMI LANDSQMI HSGUNITS lnft Population / dist=bin link=logit lrci;
repeated subject=store_id /within=ts_id type=exch corrw covb;
run;

/* From the results of genmod model we found some variables were insignificant , hence neglicting them*/

/*MODEL 4*/
proc genmod data=SSF_logson descend;
class store_id ts_id /order=formatted;
model WC(descending)= SMA Store_acc Fleet_Del TAS_Large SS_ge2_75 SS_ge10 Monthly_VOC Monthly_Phonecalls Monthly_Mktg_Adopt
                       Monthly_Avg_Tkt_YoY_Growth  Monthly_Avg_Tkt_Rev WATERSQMI lnft  / dist=bin link=logit lrci;
repeated subject=store_id /within=ts_id type=exch corrw covb;
run;
/* From the results we found that this model performs better as it has lower QIC value than the previous model*/

/*MODEL 5*/
/*gee model*/
proc gee data=SSF_logson descend;
class store_id ts_id;
model WC(descending)= SMA  Store_acc Fleet_Del store_type_RL store_type_RM TAS_Large TAS_Med SS_ge2_75 SS_ge10 Monthly_VOC Monthly_Phonecalls Monthly_Mktg_Adopt
                       Monthly_Avg_Tkt_YoY_Growth Monthly_Avg_Tkt_Rev_PnS Monthly_Avg_Tkt_Rev WATERSQMI LANDSQMI HSGUNITS lnft Population / dist=bin link=logit lrci;
repeated subject=store_id /within=ts_id type=exch;
run;
/* BETWEEN ABOVE  MODELS WE ARE CHOOSING BEST Model based on Lowest qic value WHICH IS MODEL 4*/

/* OTHER MODELS WHICH WE TRIED*/

/*MODEL 6*/
/*mixed model*/
proc mixed data=ssf_logson;
class store_id;
model WC= SMA  Store_acc Fleet_Del store_type_RL store_type_RM TAS_Large TAS_Med SS_ge2_75 SS_ge10 Monthly_VOC Monthly_Phonecalls Monthly_Mktg_Adopt
                       Monthly_Avg_Tkt_YoY_Growth Monthly_Avg_Tkt_Rev_PnS Monthly_Avg_Tkt_Rev WATERSQMI LANDSQMI HSGUNITS lnft Population/ddfm=kr s;
random int/subject=store_id;
run;
/*Comment on model:Fit criteria(AIC and BIC) not getting better*/

/*MODEL 7*/
/*GLMMIX*/
PROC GLIMMIX DATA=SSF_logson NOCLPRINT NOITPRINT GRADIENT METHOD=QUAD;
model WC(descending)= SMA PnS Store_acc Fleet_Del store_type_RL store_type_RM TAS_Large TAS_Med SS_ge2_75 SS_ge10 Monthly_VOC Monthly_Phonecalls Monthly_Mktg_Adopt
                       Monthly_Avg_Tkt_YoY_Growth Monthly_Avg_Tkt_Rev_PnS Monthly_Avg_Tkt_Rev WATERSQMI LANDSQMI HSGUNITS foottraffic Population / SOLUTION LINK=LOGIT DIST=BINARY ;

RUN; 

/*MODEL 8*/
/* RANDOM FOREST TO CHECK THE % CONTRIBUTION OF EACH FACTORS IN OVERALL MODEL*/
PROC HPFOREST DATA = SSF_logson MAXTREES = 20 SEED = 14561;
TARGET WC / LEVEL = BINARY;
INPUT SMA: PnS: Store_acc: Fleet_Del: store_type_RL: store_type_RM: TAS_Large: TAS_Med: SS_ge2_75: SS_ge10: Monthly_VOC: Monthly_Phonecalls: Monthly_Mktg_Adopt:
                       Monthly_Avg_Tkt_YoY_Growth: Monthly_Avg_Tkt_Rev_PnS: Monthly_Avg_Tkt_Rev: WATERSQMI: LANDSQMI: HSGUNITS: lnft: Population:;
ODS OUTPUT FITSTATISTICS = BCFITSTATS(RENAME = (NTREES = TREES));
RUN;

DATA BCFITSTATS;
SET BCFITSTATS;
LABEL TREES = 'NUMBER OF TREES';
LABEL MISCALL = 'FULL DATA';
LABEL MISCOOB = 'OOB';
RUN;

/*NOTE: AFTER ANALYZING ALL THE MODELS THE BEST MODEL WE FOUND IS GIVEN BY GENMOD(MODEL 4)*/

/*FOR INTEPRETATION PURPOSE WE HAVE REPLICATED MODEL 4 AGAIN*/
/*MODEL 4*/
proc genmod data=SSF_logson descend;
class store_id ts_id /order=formatted;
model WC(descending)= SMA Store_acc Fleet_Del TAS_Large SS_ge2_75 SS_ge10 Monthly_VOC Monthly_Phonecalls Monthly_Mktg_Adopt
                       Monthly_Avg_Tkt_YoY_Growth  Monthly_Avg_Tkt_Rev WATERSQMI lnft  / dist=bin link=logit lrci;
repeated subject=store_id /within=ts_id type=exch corrw covb;
run;
