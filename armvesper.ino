#include <ros.h>
#include<std_msgs/UInt16MultiArray.h>
#include <Servo.h>

Servo rarm_surv; // 右アームサーボモータ用Servoオブジェクト
Servo larm_surv; // 左アームサーボモータ用Servoオブジェクト
Servo rvesper_surv; // 左ヴェスパーサーボモータ用Servoオブジェクト
Servo lvesper_surv; // 右ヴェスパーサーボモータ用Servoオブジェクト

//ピンアサインの定義
const byte R_ARM_SERVO_PIN = 2; //右アームサーボモータ用のマイコンピン番号
const byte L_ARM_SERVO_PIN = 3; //左アームサーボモータ用のマイコンピン番号
const byte R_VESPER_SERVO_PIN = 4; //右ヴェスパーサーボモータ用のマイコンピン番号
const byte L_VESPER_SERVO_PIN = 5; //左ヴェスパーサーボモータ用のマイコンピン番号

//アームサーボモータ角度の上下限ガード値(相対値)
const int ARM_SERVOANGLE_MAX = 80; //MAX90
const int ARM_SERVOANGLE_MIN = 0;  //MIN0
//1割り込み毎に増減させるアームサーボモータ角度
const int ARM_STEPANGLE = 5;
//ヴェスパーサーボモータ角度の上下限ガード値(相対値)
const int VES_SERVOANGLE_MAX = 60; //MAX65
const int VES_SERVOANGLE_MIN = 0;  //MIN0

//左右アームサーボモータの0点調整用オフセット値(左右サーボモータ位置バラつき補正もこれで調整する)
const int R_ARMSERVO_POSOFFSET = 0; //0～90を想定
const int L_ARMSERVO_POSOFFSET = 90; //0～90を想定
//左右ヴェスパーサーボモータの0点調整用オフセット値(左右ヴェスパーモータ位置バラつき補正もこれで調整する)
const int R_VESPERSERVO_POSOFFSET = 0; //0～90を想定
const int L_VESPERSERVO_POSOFFSET = 90; //0～90を想定

//使用するDS4ボタン
const byte R1_BUTTON = 5;
const byte R2_BUTTON = 7;
const byte L1_BUTTON = 4;
const byte L2_BUTTON = 6;
const byte R3_BUTTON = 11;
const byte L3_BUTTON = 10;
const byte SH_BUTTON = 8;
const byte OP_BUTTON = 9;

//状態定数定義
const int REST = 0;
const int RARM_MV1 = 10;
const int RARM_MV2 = 20;
const int LARM_MV1 = 30;
const int LARM_MV2 = 40;
const int VESPER_MV1 = 50;
const int VESPER_MV2 = 60;

//状態変数定義
int mvstate = REST;

//左右アーム・左右ヴェスパーサーボ位置変数
int rarm_srvpos = 0;
int larm_srvpos = 90;
int rvesper_srvpos = 0;
int lvesper_srvpos = 90;

//ROS関連定義
ros::NodeHandle nh; //ROSノードのインスタンス宣言

//関数定義
void restfunc( const std_msgs::UInt16MultiArray btnmsg )
{
  if ( btnmsg.data[R2_BUTTON] == 1 )
  {
    mvstate = RARM_MV1;
    rarm_surv.write( ( rarm_srvpos + R_ARMSERVO_POSOFFSET ) );
    delay( 20 );
  }
  else if ( btnmsg.data[R1_BUTTON] == 1 )
  {
    mvstate = RARM_MV2;
    rarm_surv.write( ( rarm_srvpos + R_ARMSERVO_POSOFFSET ) );
    delay( 20 );
  }
  else if ( btnmsg.data[L1_BUTTON] == 1 )
  {
    mvstate = LARM_MV1;
    larm_surv.write( ( larm_srvpos + L_ARMSERVO_POSOFFSET ) );
    delay( 20 );
  }
  else if ( btnmsg.data[L2_BUTTON] == 1 )
  {
    mvstate = LARM_MV2;
    larm_surv.write( ( larm_srvpos + L_ARMSERVO_POSOFFSET ) );
    delay( 20 );
  }
  else if ( btnmsg.data[R3_BUTTON] == 1 )
  {
    mvstate = VESPER_MV1;
    rvesper_surv.write( ( rvesper_srvpos + R_VESPERSERVO_POSOFFSET ) );
    lvesper_surv.write( ( lvesper_srvpos + L_VESPERSERVO_POSOFFSET ) );
    delay( 20 );
  }
  else if ( btnmsg.data[L3_BUTTON] == 1 )
  {
    mvstate = VESPER_MV2;
    rvesper_surv.write( ( rvesper_srvpos + R_VESPERSERVO_POSOFFSET ) );
    lvesper_surv.write( ( lvesper_srvpos + L_VESPERSERVO_POSOFFSET ) );
    delay( 20 );
  }
  else
  {
    mvstate = REST;
  }
}

void rarm_mv1func( int btnmsg )
{
  if ( btnmsg != 1 )
  {
    mvstate = REST;
  }
  else
  {
    if ( rarm_srvpos < ARM_SERVOANGLE_MAX )
    {
      rarm_srvpos = rarm_srvpos + ARM_STEPANGLE;
    }
    else
    {
      rarm_srvpos = ARM_SERVOANGLE_MAX;
    }
    rarm_surv.write( ( rarm_srvpos + R_ARMSERVO_POSOFFSET ) );
    delay( 20 );
  }
}

void rarm_mv2func( int btnmsg )
{
  if ( btnmsg != 1 )
  {
    mvstate = REST;
  }
  else
  {
    if ( rarm_srvpos > ARM_SERVOANGLE_MIN )
    {
      rarm_srvpos = rarm_srvpos - ARM_STEPANGLE;
    }
    else
    {
      rarm_srvpos = ARM_SERVOANGLE_MIN;
    }
    rarm_surv.write( ( rarm_srvpos + R_ARMSERVO_POSOFFSET ) );
    delay( 20 );
  }
}

void larm_mv1func( int btnmsg )
{
  if ( btnmsg != 1 )
  {
    mvstate = REST;
  }
  else
  {
    if ( larm_srvpos < ARM_SERVOANGLE_MAX )
    {
      larm_srvpos = larm_srvpos + ARM_STEPANGLE;
    }
    else
    {
      larm_srvpos = ARM_SERVOANGLE_MAX;
    }
    larm_surv.write( ( larm_srvpos + L_ARMSERVO_POSOFFSET ) );
    delay( 20 );
  }
}

void larm_mv2func( int btnmsg )
{
  if ( btnmsg != 1 )
  {
    mvstate = REST;
  }
  else
  {
    if ( larm_srvpos > ARM_SERVOANGLE_MIN )
    {
      larm_srvpos = larm_srvpos - ARM_STEPANGLE;
    }
    else
    {
      larm_srvpos = ARM_SERVOANGLE_MIN;
    }
    larm_surv.write( ( larm_srvpos + L_ARMSERVO_POSOFFSET ) );
    delay( 20 );
  }
}

void vesper_mv1func( int btnmsg )
{
  if ( btnmsg != 1 )
  {
    mvstate = REST;
  }
  else
  {
    if ( rvesper_srvpos > VES_SERVOANGLE_MIN )
    {
      rvesper_srvpos = rvesper_srvpos - 5;
      //lvesper_srvpos = rvesper_srvpos; 
      lvesper_srvpos = lvesper_srvpos + 5;
    }
    else
    {
      rvesper_srvpos = VES_SERVOANGLE_MIN;
      lvesper_srvpos = VES_SERVOANGLE_MAX;
    }
    rvesper_surv.write( ( rvesper_srvpos + R_VESPERSERVO_POSOFFSET ) );
    lvesper_surv.write( ( lvesper_srvpos + L_VESPERSERVO_POSOFFSET ) );
    delay( 20 );
  }
}

void vesper_mv2func( int btnmsg )
{
  if ( btnmsg != 1 )
  {
    mvstate = REST;
  }
  else
  {
    if ( rvesper_srvpos < VES_SERVOANGLE_MAX )
    {
      rvesper_srvpos = rvesper_srvpos + 5;
      //lvesper_srvpos = rvesper_srvpos;
      lvesper_srvpos = lvesper_srvpos - 5;
    }
    else
    {
      rvesper_srvpos = VES_SERVOANGLE_MAX;
      lvesper_srvpos = VES_SERVOANGLE_MIN;
    }
    rvesper_surv.write( ( rvesper_srvpos + R_VESPERSERVO_POSOFFSET ) );
    lvesper_surv.write( ( lvesper_srvpos + L_VESPERSERVO_POSOFFSET ) );
    delay( 20 );
  }
}

void ds4msgcb( const std_msgs::UInt16MultiArray& ds4msg )
{
  switch(mvstate)
  {
    case REST:
      restfunc(ds4msg);
      break;
    case RARM_MV1:
      rarm_mv1func( (int)ds4msg.data[R2_BUTTON] );
      break;
    case RARM_MV2:
      rarm_mv2func( (int)ds4msg.data[R1_BUTTON] );
      break;
    case LARM_MV1:
      larm_mv1func( (int)ds4msg.data[L1_BUTTON] );
      break;
    case LARM_MV2:
      larm_mv2func( (int)ds4msg.data[L2_BUTTON] );
      break;
    case VESPER_MV1:
      vesper_mv1func( (int)ds4msg.data[R3_BUTTON] );
      break;
    case VESPER_MV2:
      vesper_mv2func( (int)ds4msg.data[L3_BUTTON] );
      break;
    default:
      restfunc(ds4msg);
      break;
  }
}

ros::Subscriber<std_msgs::UInt16MultiArray> sub( "ds4btns", ds4msgcb ); //サブスクライバのインスタンスsubの定義
//debug code
std_msgs::UInt16MultiArray dbg_msg; //パブリッシュするデバッグ用メッセージ
ros::Publisher pub_debug( "debug_amvs", &dbg_msg );  //パブリッシャーのインスタンスpub_debugの定義

void setup()
{
  //ROSノード初期化
  nh.initNode();
  nh.subscribe(sub); //サブスクライバのインスタンスsubの作成
  //debug code
  nh.advertise(pub_debug); //パブリッシャーのインスタンスpub_debugの作成
  //パブリッシュする配列型メッセージのサイズ設定
  dbg_msg.data_length = 5;
  dbg_msg.data = (int16_t *)malloc(sizeof(int16_t)*5);
  //サーボ用出力ピン設定
  rarm_surv.attach(R_ARM_SERVO_PIN);
  larm_surv.attach(L_ARM_SERVO_PIN);
  rvesper_surv.attach(R_VESPER_SERVO_PIN);
  lvesper_surv.attach(L_VESPER_SERVO_PIN);
  
  //サーボ初期位置設定
  rarm_surv.write( ( rarm_srvpos + R_ARMSERVO_POSOFFSET ) );
  larm_surv.write( ( larm_srvpos + L_ARMSERVO_POSOFFSET ) );
  rvesper_surv.write( ( rvesper_srvpos + R_VESPERSERVO_POSOFFSET ) );
  lvesper_surv.write( ( lvesper_srvpos + L_VESPERSERVO_POSOFFSET ) );
}

void loop()
{
  //debug code
  dbg_msg.data[0] = mvstate;
  dbg_msg.data[1] = rarm_srvpos;
  dbg_msg.data[2] = larm_srvpos;
  dbg_msg.data[3] = rvesper_srvpos;
  dbg_msg.data[4] = lvesper_srvpos;
  pub_debug.publish( &dbg_msg );
  
  nh.spinOnce();
  delay( 10 );
}

