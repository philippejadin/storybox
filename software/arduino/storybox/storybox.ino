/**
Story box

Code pour la boite à histoire, version arduino.

Librairies utilisées :
https://github.com/LennartHennigs/Button2
https://github.com/pschatzmann/arduino-audio-tools
https://github.com/pschatzmann/arduino-libhelix
 */

#include <SPI.h>
#include <SDFS.h>
#include "AudioTools.h"
#include "AudioCodecs/CodecMP3Helix.h"
#include "Button2.h"

/***************** CONFIG *******************/

// max number of stories in a directory
#define MAXSTORIES 20

// max volume
#define MAX_VOLUME 1024 // 0..1024

/****************** no more config below vvvv **************/

/********************** HARDWARE PINS *************************/
#define SDCARD_SPI SPI
#define SDCARD_CS_PIN 17

#define VOLUME_PIN 27
#define BUTTON_LEFT_PIN 10
#define BUTTON_RIGHT_PIN 11
#define BUTTON_PLAY_PIN 12
#define BUTTON_HOME_PIN 13

#define I2S_BCK 20
#define I2S_WS 21
#define I2S_DATA 22

#define BATTERY_ADC_PIN 26

#define BTN_DEBOUNCE_MS 10

// #define SPI_CLOCK SD_SCK_MHZ(40)
// #define MP3_MAX_OUTPUT_SIZE 1024
// #define MP3_MAX_FRAME_SIZE 800

//#define SPI_CLOCK SD_SCK_MHZ(20)
//#define MP3_MAX_OUTPUT_SIZE 1024 * 5 // 1024 * 5
//#define MP3_MAX_FRAME_SIZE 3200      // 1600
//#define I2S_BUFFER_SIZE 1024

#define COPIER_BUFFER_SIZE 512

/* end hardware config */

I2SStream i2s;
VolumeStream volumer(i2s);
EncodedAudioStream decoder(&volumer, new MP3DecoderHelix());
File audioFile;
StreamCopy copier(decoder, audioFile, COPIER_BUFFER_SIZE);

#define is_menu 0
#define is_play 1
#define is_pause 2

int status = is_menu;

Button2 button_home;
Button2 button_left;
Button2 button_right;
Button2 button_play;

String currentpath = "";

int currentstory = 1;
int totalstories = 0;

String stories[MAXSTORIES];

float volume = 0.5;

void setup()
{
  // logger
  Serial.begin(115200);
  AudioLogger::instance().begin(Serial, AudioLogger::Info);

  SDFSConfig sdconfig;
  sdconfig.setCSPin(SDCARD_CS_PIN);
  SDFS.setConfig(sdconfig);

  if (!SDFS.begin())
  {
    Serial.printf("Init sd failed\n");
  }

  delay(100);
  Serial.printf("Story Box start\n");
  delay(100);

  // i2s
  auto config = i2s.defaultConfig(TX_MODE);
  config.pin_bck = I2S_BCK;
  config.pin_ws = I2S_WS;
  config.pin_data = I2S_DATA;
  i2s.begin(config);

  // setup I2S based on sampling rate provided by decoder
  decoder.setNotifyAudioChange(i2s);
  decoder.begin();

  // copier buffer size
  //copier.resize(COPIER_BUFFER_SIZE);

  // volume
  volume = float(MAX_VOLUME) / 1024;
  volumer.begin(config); // we need to provide the bits_per_sample and channels
  volumer.setVolume(volume);

  // buttons
  button_left.begin(BUTTON_LEFT_PIN);
  button_left.setPressedHandler(handleTapLeft);

  button_right.begin(BUTTON_RIGHT_PIN);
  button_right.setPressedHandler(handleTapRight);

  button_home.begin(BUTTON_HOME_PIN);
  button_home.setPressedHandler(handleTapHome);

  button_play.begin(BUTTON_PLAY_PIN);
  button_play.setPressedHandler(handleTapPlay);

  // experimental interupt code, not needed anymore since the copier buffer size is lowered, loop rusn fast enough now
  /*
    attachInterrupt(digitalPinToInterrupt(BUTTON_LEFT_PIN), handleinterrupt, CHANGE);
    attachInterrupt(digitalPinToInterrupt(BUTTON_RIGHT_PIN), handleinterrupt, CHANGE);
    attachInterrupt(digitalPinToInterrupt(BUTTON_HOME_PIN), handleinterrupt, CHANGE);
    attachInterrupt(digitalPinToInterrupt(BUTTON_PLAY_PIN), handleinterrupt, CHANGE);
  */

  handleDirectoryChange();
  play("/intro.mp3");
}

void handleinterrupt()
{
  button_left.loop();
  button_right.loop();
  button_home.loop();
  button_play.loop();
}

void play(String filename)
{
  audioFile = SDFS.open(filename, "r");
  copier.begin(decoder, audioFile);
  Serial.print("Play start ");
  Serial.println(filename);
}

void playmenu()
{
  status = is_menu;
  String menu = "/menu.mp3";
  play(currentpath + '/' + stories[currentstory] + menu);
}

void playstory()
{
  if (status == is_pause)
  {
    status = is_play;
    return;
  }
  status = is_play;
  play(currentpath + '/' + stories[currentstory] + "/story.mp3");
}

// currentpath
// currentstory = 1 .. int
// totalstories = int
// liste des dossier dans le dossier actuel -> tableau -> stories

void debug()
{
  Serial.print("Current path : ");
  Serial.println(currentpath);
  Serial.print("totalstories : ");
  Serial.println(totalstories);
  Serial.print("Current story : ");
  Serial.println(currentstory);
  Serial.println("Stories found : ");
  for (int i = 0; i < totalstories; i++)
  {
    Serial.print("- ");
    Serial.println(stories[i]);
  }
  if (status == is_play)
  {
    Serial.println("*** playing ****");
  }

  if (status == is_menu)
  {
    Serial.println("*** on menu ****");
  }

  if (status == is_pause)
  {
    Serial.println("*** paused ****");
  }

  handleTemperature();
  handleBattery();
  Serial.print("Volume : ");
  Serial.println(volume);

  Serial.println("-----------------");
}

void handleDirectoryChange()
{
  totalstories = 0;
  Dir dir = SDFS.openDir(currentpath);
  while (dir.next())
  {
    if (dir.isDirectory())
    {
      stories[totalstories] = dir.fileName();
      totalstories++;
    }
  }
}

void handleTapLeft(Button2 &b)
{
  Serial.println("button left pressed");
  currentstory--;
  if (currentstory < 0)
  {
    currentstory = totalstories - 1;
  }
  int i = 0;

  playmenu();
  debug();
}

void handleTapRight(Button2 &b)
{
  Serial.println("button right pressed");
  currentstory++;
  if (currentstory >= totalstories)
  {
    currentstory = 0;
  }
  playmenu();
  debug();
}

void handleTapHome(Button2 &b)
{
  Serial.println("button home pressed");
  currentpath = "";
  handleDirectoryChange();
  debug();
}

void handleTapPlay(Button2 &b)
{
  Serial.println("button play pressed");
  if (status == is_play)
  {
    status = is_pause;
  }
  else
  {
    playstory();
  }
  debug();
}

float lastVolume;

void handleVolume()
{
  int volumeraw = analogRead(VOLUME_PIN);

  volume = float(map(volumeraw, 0, 1024, 0, MAX_VOLUME)) / 1024.0;
  if (volume != lastVolume)
  {
    lastVolume = volume;
    volumer.setVolume(volume);
    // Serial.print("Volume : ");
    // Serial.println(volume);
  }
}

void handleBattery()
{
  float vsys = float(analogRead(29)) * 3.0 * 3.3 / 1024;
  Serial.print("vsys : ");
  Serial.println(vsys);

  float battery = float(analogRead(BATTERY_ADC_PIN)) * 2.0 * 3.3 / 1024 + 0.15; // the 0.15 is to acknowledge the voltage drop from the schotky diode
  Serial.print("battery : ");
  Serial.println(battery);
}

void handleTemperature()
{
  int temperature = analogReadTemp();
  Serial.print("Temperature : ");
  Serial.println(temperature);
}

void loop()
{
  button_left.loop();
  button_right.loop();
  button_home.loop();
  button_play.loop();

  if (status == is_play || status == is_menu)
  {
    copier.copy();
    handleVolume();
  }
}
