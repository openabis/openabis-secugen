# encoding: utf-8
import os
import platform

from cffi import FFI

TEMPLATE_FORMAT_ISO19794 = "iso19794"

ffi = FFI()

ffi.cdef(
    """
#define NULL 0
typedef void*           HWND;
typedef void*           HDC;
typedef unsigned long   DWORD;
typedef int             BOOL;
typedef unsigned char   BYTE;
typedef unsigned short  WORD;
typedef struct
{
    int left, top, right, bottom;
} RECT;
typedef RECT* LPRECT;
enum SGFDxDeviceName
{
   SG_DEV_UNKNOWN = 0,
   SG_DEV_FDP02 = 0x01,
   SG_DEV_FDU02 = 0x03,
   SG_DEV_FDU03 = 0x04,
   SG_DEV_FDU04 = 0x05,
   SG_DEV_FDU05 = 0x06,
   SG_DEV_AUTO = 0xFF,
};
enum SGPPPortAddr {
   AUTO_DETECT = 0,
   LPT1        = 0x378,
   LPT2        = 0x278,
   LPT3        = 0x3BC,
   USB_AUTO_DETECT = 0x3BD,
};
enum SGFDxSecurityLevel
{
   SL_NONE = 0,
   SL_LOWEST = 1,
   SL_LOWER = 2,
   SL_LOW = 3,
   SL_BELOW_NORMAL = 4,
   SL_NORMAL = 5,
   SL_ABOVE_NORMAL = 6,
   SL_HIGH = 7,
   SL_HIGHER = 8,
   SL_HIGHEST = 9,
};
enum SGFDxTemplateFormat
{
   TEMPLATE_FORMAT_ANSI378 = 0x0100,
   TEMPLATE_FORMAT_SG400   = 0x0200,
   TEMPLATE_FORMAT_ISO19794 = 0x0300,
};
enum SGCallBackFuntion {
   CALLBACK_LIVE_CAPTURE = 1,
   CALLBACK_AUTO_ON_EVENT = 2,
};
enum SGFDxErrorCode {
   // General error
   SGFDX_ERROR_NONE = 0,
   SGFDX_ERROR_CREATION_FAILED = 1,
   SGFDX_ERROR_FUNCTION_FAILED = 2,
   SGFDX_ERROR_INVALID_PARAM = 3,
   SGFDX_ERROR_NOT_USED = 4,
   SGFDX_ERROR_DLLLOAD_FAILED = 5,
   SGFDX_ERROR_DLLLOAD_FAILED_DRV = 6,
   SGFDX_ERROR_DLLLOAD_FAILED_ALGO = 7,
   // Device error
   SGFDX_ERROR_SYSLOAD_FAILED = 51, // system file load fail
   SGFDX_ERROR_INITIALIZE_FAILED = 52,   // chip initialize fail
   SGFDX_ERROR_LINE_DROPPED = 53,        // image data drop
   SGFDX_ERROR_TIME_OUT = 54,            // getliveimage timeout error
   SGFDX_ERROR_DEVICE_NOT_FOUND = 55,    // device not found
   SGFDX_ERROR_DRVLOAD_FAILED = 56,      // dll file load fail
   SGFDX_ERROR_WRONG_IMAGE = 57,         // wrong image
   SGFDX_ERROR_LACK_OF_BANDWIDTH = 58,   // USB Bandwith Lack Error
   SGFDX_ERROR_DEV_ALREADY_OPEN = 59,    // Device Exclusive access Error
   SGFDX_ERROR_GETSN_FAILED = 60,         // Fail to get Device Serial Number
   SGFDX_ERROR_UNSUPPORTED_DEV = 61,      // Unsupported device

   // Extract &Matching error
   SGFDX_ERROR_FEAT_NUMBER = 101,  // too small number of minutiae
   SGFDX_ERROR_INVALID_TEMPLATE_TYPE = 102,      // wrong template type
   SGFDX_ERROR_INVALID_TEMPLATE1 = 103,         //error in decoding template 1
   SGFDX_ERROR_INVALID_TEMPLATE2 = 104,         //error in decoding template 2
   SGFDX_ERROR_EXTRACT_FAIL = 105,
   SGFDX_ERROR_MATCH_FAIL = 106
};
enum SGImpressionType
{
   SG_IMPTYPE_LP =	0x00,		// Live-scan plain
   SG_IMPTYPE_LR =	0x01,		// Live-scan rolled
   SG_IMPTYPE_NP =	0x02,		// Nonlive-scan plain
   SG_IMPTYPE_NR =	0x03,		// Nonlive-scan rolled
};
enum SGFingerPosition
{
   SG_FINGPOS_UK = 0x00,		// Unknown finger
   SG_FINGPOS_RT = 0x01,		// Right thumb
   SG_FINGPOS_RI = 0x02,		// Right index finger
   SG_FINGPOS_RM = 0x03,		// Right middle finger
   SG_FINGPOS_RR = 0x04,		// Right ring finger
   SG_FINGPOS_RL = 0x05,		// Right little finger
   SG_FINGPOS_LT = 0x06,		// Left thumb
   SG_FINGPOS_LI = 0x07,		// Left index finger
   SG_FINGPOS_LM = 0x08,		// Left middle finger
   SG_FINGPOS_LR = 0x09,		// Left ring finger
   SG_FINGPOS_LL = 0x0A,		// Left little finger
};
#define SGDEV_SN_LEN          15   // Device Serial Number Length
// For AutoOn event
#define WM_APP_SGAUTOONEVENT    0x8100  // From ISensor.h
#define SGDEVEVNET_FINGER_OFF   0
#define SGDEVEVNET_FINGER_ON    1
// EnumerateDevice()
typedef struct tagSGDeviceList
{
   DWORD DevName;
   DWORD DevID;
   WORD  DevType;
   BYTE  DevSN[16];
} SGDeviceList;
typedef SGDeviceList *LPDeviceList;
// GetDeviceInfo()
typedef struct tagSGDeviceInfoParam
{
   DWORD DeviceID;         // 0 - 9
   BYTE  DeviceSN[16];         // Device Serial Number, Length of SN = 15
   DWORD ComPort;          // Parallel device=>PP address, USB device=>USB(0x3BC+1)
   DWORD ComSpeed;         // Parallel device=>PP mode, USB device=>0
   DWORD ImageWidth;       // Image Width
   DWORD ImageHeight;      // Image Height
   DWORD Contrast; 	      // 0 ~ 100
   DWORD Brightness;       // 0 ~ 100
   DWORD	Gain;             // Dependent on each device
   DWORD ImageDPI;         // DPI
   DWORD FWVersion;        // FWVersion
} SGDeviceInfoParam;
typedef SGDeviceInfoParam* LPSGDeviceInfoParam;
typedef struct tagSGFingerInfo {
    WORD FingerNumber;			// FingerNumber.
    WORD ViewNumber;           // Sample number
    WORD ImpressionType;       // impression type. Should be 0
    WORD ImageQuality;         // Image quality
} SGFingerInfo;
typedef struct tagSGANSITemplateInfo {
    DWORD TotalSamples;
    SGFingerInfo SampleInfo[225];		//max finger number 15 x max view number 15 = 225
} SGANSITemplateInfo, SGISOTemplateInfo;
typedef struct tagSGCBLiveCaptureParam {
   DWORD  ImageWidth;
   DWORD  ImageHeight;
   DWORD  Quality;
   DWORD  ErrorCode;
} SGCBLiveCaptureParam;
// 2006.10.9, Used in CreateTemplate2()
typedef struct tagSGFPImageInfo {
    WORD CaptureEquip;            // capture equipment ID
    WORD ImageSizeInX;            // in pixels
    WORD ImageSizeInY;            // in pixels
    WORD XResolution;             // in pixels per cm 500dpi = 197
    WORD YResolution;             // in pixels per cm
    WORD FingerNumber;			// capture equipment ID
    WORD ViewNumber;            // in pixels
    WORD ImpressionType;            // in pixels
    WORD ImageQuality;             // in pixels per cm 500dpi = 197
} SGFPImageInfo;
typedef struct tagSGANSITemplateInfoEx {
    DWORD TotalSamples;
    SGFPImageInfo SampleInfo[225];		//max finger number 15 x max view number 15 = 225
} SGANSITemplateInfoEx, SGISOTemplateInfoEx;
typedef void*  HSGFPM;
 DWORD   SGFPM_Create(HSGFPM* phFPM);
 DWORD   SGFPM_Terminate(HSGFPM hFpm);
 DWORD   SGFPM_Init(HSGFPM hFpm, DWORD devName);
 DWORD   SGFPM_InitEx(HSGFPM hFpm, DWORD width, DWORD height, DWORD dpi);
 DWORD   SGFPM_SetTemplateFormat(HSGFPM hFpm, WORD format); // default is ANSI378
 DWORD   SGFPM_GetLastError(HSGFPM hFpm);
// Image sensor API
 DWORD   SGFPM_EnumerateDevice(HSGFPM hFpm, DWORD* ndevs, SGDeviceList** devList);
 DWORD   SGFPM_OpenDevice(HSGFPM hFpm, DWORD devId);
 DWORD   SGFPM_CloseDevice(HSGFPM hFpm);
 DWORD   SGFPM_GetDeviceInfo(HSGFPM hFpm, SGDeviceInfoParam* pInfo);
 DWORD   SGFPM_Configure(HSGFPM hFpm, HWND hwnd);
 DWORD   SGFPM_SetBrightness(HSGFPM hFpm, DWORD brightness);
 DWORD   SGFPM_SetLedOn(HSGFPM hFpm, bool on);
 DWORD   SGFPM_GetImage(HSGFPM hFpm, BYTE* buffer);
 DWORD   SGFPM_GetImageEx(HSGFPM hFpm, BYTE* buffer, DWORD time, HWND dispWnd, DWORD quality);
 DWORD   SGFPM_GetImageEx2(HSGFPM hFpm, BYTE* buffer, DWORD time, HDC dispDC, LPRECT dispRect, DWORD quality);
 DWORD   SGFPM_GetImageQuality(HSGFPM hFpm, DWORD width, DWORD height, BYTE* imgBuf, DWORD* quality);
 DWORD   SGFPM_SetCallBackFunction(
            HSGFPM hFpm, DWORD selector, DWORD (*)(void* pUserData, void* pCallBackData), void* pUserData);
// FDU03 or Later device Only APIs
 DWORD   SGFPM_EnableAutoOnEvent(HSGFPM hFpm, BOOL enable, HWND hwnd, void* reserved);
// Algorithm: Extraction API
 DWORD   SGFPM_GetMaxTemplateSize(HSGFPM hFpm, DWORD* size);
 DWORD   SGFPM_CreateTemplate(HSGFPM hFpm, SGFingerInfo* fpInfo, BYTE *rawImage, BYTE* minTemplate);
 DWORD   SGFPM_GetTemplateSize(HSGFPM hFpm, BYTE* minTemplate, DWORD* size);
// Algorithm: Matching API
 DWORD   SGFPM_MatchTemplate(HSGFPM hFpm, BYTE *minTemplate1, BYTE *minTemplate2, DWORD secuLevel, BOOL* matched);
 DWORD   SGFPM_GetMatchingScore(HSGFPM hFpm, BYTE* minTemplate1, BYTE* minTemplate2, DWORD* score);
// Algorithim: Only work with ANSI378 Template
 DWORD    SGFPM_GetTemplateSizeAfterMerge(HSGFPM hFpm, BYTE* ansiTemplate1, BYTE* ansiTemplate2, DWORD* size);
 DWORD    SGFPM_MergeAnsiTemplate(HSGFPM hFpm, BYTE* ansiTemplate1, BYTE* ansiTemplate2, BYTE* outTemplate);
 DWORD    SGFPM_MergeMultipleAnsiTemplate(HSGFPM hFpm, BYTE* inTemplates, DWORD nTemplates, BYTE* outTemplate);
 DWORD    SGFPM_GetAnsiTemplateInfo(HSGFPM hFpm, BYTE* ansiTemplate, SGANSITemplateInfo* templateInfo);
 DWORD    SGFPM_MatchAnsiTemplate(HSGFPM hFpm, BYTE* ansiTemplate1, DWORD sampleNum1, BYTE* ansiTemplate2,
 DWORD  sampleNum2, DWORD  secuLevel, BOOL*  matched);
 DWORD    SGFPM_GetAnsiMatchingScore(HSGFPM hFpm, BYTE* ansiTemplate1, DWORD  sampleNum1, BYTE* ansiTemplate2,
 DWORD    sampleNum2, DWORD* score);
 DWORD    SGFPM_MatchTemplateEx(HSGFPM hFpm, BYTE* minTemplate1, WORD   tempateType1,
 DWORD  sampleNum1, BYTE* minTemplate2, WORD   tempateType2,  DWORD sampleNum2, DWORD  secuLevel, BOOL*  matched);
 DWORD    SGFPM_GetMatchingScoreEx(HSGFPM hFpm, BYTE* minTemplate1, WORD tempateType1,
 DWORD sampleNum1, BYTE* minTemplate2, WORD tempateType2, DWORD sampleNum2, DWORD* score);
 DWORD    SGFPM_SetAutoOnIRLedTouchOn(HSGFPM hFpm, BOOL iRLed, BOOL touchOn);
 DWORD    SGFPM_GetMinexVersion(HSGFPM hFpm, DWORD *extractor, DWORD* matcher);
 DWORD    SGFPM_CreateTemplateEx(HSGFPM hFpm, SGFPImageInfo* fpImageInfo, BYTE *rawImage, BYTE* minTemplate);
 DWORD    SGFPM_GetAnsiTemplateInfoEx(HSGFPM hFpm, BYTE* ansiTemplate, SGANSITemplateInfoEx* templateInfo);
// Algorithim: Only work with ISO19794 Template
 DWORD    SGFPM_GetIsoTemplateSizeAfterMerge(HSGFPM hFpm, BYTE* isoTemplate1, BYTE* isoTemplate2, DWORD* size);
 DWORD    SGFPM_MergeIsoTemplate(HSGFPM hFpm, BYTE* isoTemplate1, BYTE* isoTemplate2, BYTE* outTemplate);
 DWORD    SGFPM_MergeMultipleIsoTemplate(HSGFPM hFpm, BYTE* inTemplates, DWORD nTemplates, BYTE* outTemplate);
 DWORD    SGFPM_GetIsoTemplateInfo(HSGFPM hFpm, BYTE* isoTemplate, SGISOTemplateInfo* templateInfo);
 DWORD    SGFPM_MatchIsoTemplate(HSGFPM hFpm, BYTE* isoTemplate1, DWORD sampleNum1, BYTE* isoTemplate2,
 DWORD  sampleNum2, DWORD  secuLevel, BOOL*  matched);
 DWORD    SGFPM_GetIsoMatchingScore(HSGFPM hFpm, BYTE* isoTemplate1, DWORD  sampleNum1, BYTE* isoTemplate2,
 DWORD sampleNum2, DWORD* score);
// 06/08/2009, Enable/disable the check of finger liveness
 DWORD 	  SGFPM_EnableCheckOfFingerLiveness(HSGFPM hFpm, BOOL enable);
// 05/19/2011, Adjust fake detection level
 DWORD 	  SGFPM_SetFakeDetectionLevel(HSGFPM hFpm, int level);
// 05/27/2011, Get fake detection level
 DWORD 	  SGFPM_GetFakeDetectionLevel(HSGFPM hFpm, int *level);
// 09/09/2011, Send commands to device
 DWORD 	  SGFPM_WriteData(HSGFPM hFpm, unsigned char index, unsigned char data);
"""
)  # noqa

try:
    import sys

    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
    current_dirname = os.path.join(base_path, "secugen")
except Exception:
    current_dirname = os.path.dirname(os.path.abspath(__file__))

try:
    import win32api

    win32api.SetDllDirectory(current_dirname)
except:  # noqa
    pass

platform_name = platform.system().lower()


def get_libraries(config):

    if platform_name == "linux":
        ffi.dlopen("libstdc++.so.6", ffi.RTLD_GLOBAL)
        ffi.dlopen("libusb-0.1.so.4", ffi.RTLD_GLOBAL)
        ffi.dlopen(config['LIBSGFDU03'], ffi.RTLD_GLOBAL)
        ffi.dlopen(config['LIBSGFPAMX'], ffi.RTLD_GLOBAL)
        sgfplib = ffi.dlopen(config['LIBSGFPLIB'])
    elif platform_name == "darwin":
        sgfplib = None
    else:
        sgfplib = ffi.dlopen(config['SGFPLIB'])

    return sgfplib


class SecuGen:
    SECURITY_LEVEL_NONE = 0
    SECURITY_LEVEL_LOWEST = 1
    SECURITY_LEVEL_LOWER = 2
    SECURITY_LEVEL_LOW = 3
    SECURITY_LEVEL_BELOW_NORMAL = 4
    SECURITY_LEVEL_NORMAL = 5
    SECURITY_LEVEL_ABOVE_NORMAL = 6
    SECURITY_LEVEL_HIGH = 7
    SECURITY_LEVEL_HIGHER = 8
    SECURITY_LEVEL_HIGHEST = 9

    TEMPLATE_FORMAT_ANSI378 = 0x0100
    TEMPLATE_FORMAT_SG400 = 0x0200
    TEMPLATE_FORMAT_ISO19794 = 0x0300

    def __init__(self, config):

        self.input_format = TEMPLATE_FORMAT_ISO19794
        self.secu_level = config.get("SECUGEN_MATCH_SECURITY_LEVEL", self.SECURITY_LEVEL_NORMAL)
        self.fpm = ffi.new("HSGFPM*")
        self.sgfplib = get_libraries(config)
        if self.sgfplib is None:
            raise Exception("No SecuGen library has been loaded")
        err = self.sgfplib.SGFPM_Create(self.fpm)
        if err != 0:
            raise Exception("SGFPM_Create error: {}".format(err))

        self.init_extraction()

    def init_extraction(self, width=260, height=300, dpi=500, template_format=TEMPLATE_FORMAT_ISO19794):
        self.sgfplib.SGFPM_InitEx(self.fpm[0], width, height, dpi)
        err = self.sgfplib.SGFPM_SetTemplateFormat(self.fpm[0], template_format)
        if err != 0:
            raise Exception("SGFPM_SetTemplateFormat error: {}".format(err))

    def merge_multiple_templates(self, templates):
        total_size = 0
        for template in templates:
            total_size += len(template)

        source_template = ffi.new("BYTE[]", total_size)

        offset = 0
        for template in templates:
            tempalte_len = len(template)
            ffi.memmove(source_template + offset, template, tempalte_len)
            offset += tempalte_len

        target_template = ffi.new("BYTE[]", len(source_template))
        err = self.sgfplib.SGFPM_MergeMultipleIsoTemplate(self.fpm[0], source_template, len(templates), target_template)
        if err != 0:
            raise Exception("SGFPM_MergeMultipleIsoTemplate error: {}".format(err))
        real_size = ffi.new("DWORD*")
        err = self.sgfplib.SGFPM_GetTemplateSize(self.fpm[0], target_template, real_size)
        if err != 0:
            raise Exception("SGFPM_GetTemplateSize error: {}".format(err))
        return ffi.buffer(target_template)[0 : real_size[0]]

    def get_iso_template_info(self, template):
        sample_info = ffi.new("SGISOTemplateInfo*")
        err = self.sgfplib.SGFPM_GetIsoTemplateInfo(self.fpm[0], template, sample_info)
        if err != 0:
            raise Exception("SGFPM_GetIsoTemplateInfo error: {}".format(err))
        print("Found {} sub-templates:".format(sample_info[0].TotalSamples))
        for i in range(sample_info[0].TotalSamples):
            print(
                "\t- Template {}: FingerNumber={}, ViewNumber={}, ImpressionType={}, ImageQuality={}".format(
                    i,
                    sample_info[0].SampleInfo[i].FingerNumber,
                    sample_info[0].SampleInfo[i].ViewNumber,
                    sample_info[0].SampleInfo[i].ImpressionType,
                    sample_info[0].SampleInfo[i].ImageQuality,
                )
            )

    def create_template(self, raw_image, finger_position=0):
        size = ffi.new("DWORD*")
        err = self.sgfplib.SGFPM_GetMaxTemplateSize(self.fpm[0], size)
        if err != 0:
            raise Exception("SGFPM_GetMaxTemplateSize error: {}".format(err))

        finger_info = ffi.new(
            "SGFingerInfo*", {"FingerNumber": finger_position, "ViewNumber": 0, "ImpressionType": 0, "ImageQuality": 0}
        )
        template = ffi.new("BYTE[]", size[0])
        err = self.sgfplib.SGFPM_CreateTemplate(self.fpm[0], finger_info, raw_image, template)
        if err != 0:
            raise Exception("SGFPM_CreateTemplate error: {}".format(err))

        real_size = ffi.new("DWORD*")
        err = self.sgfplib.SGFPM_GetTemplateSize(self.fpm[0], template, real_size)
        if err != 0:
            raise Exception("SGFPM_GetTemplateSize error: {}".format(err))
        return ffi.buffer(template)[0 : real_size[0]]

    def match_templates(self, fingerprint1, fingerprint2):
        score = ffi.new("DWORD*")
        err = self.sgfplib.SGFPM_GetMatchingScoreEx(
            self.fpm[0],
            fingerprint1,
            self.TEMPLATE_FORMAT_ISO19794,
            0,
            fingerprint2,
            self.TEMPLATE_FORMAT_ISO19794,
            0,
            score,
        )
        if err != 0:
            print("SGFPM_MatchTemplateEx error: {}".format(err))
            return 0
        return score[0] / 200

    def get_quality(self, width, height, img):
        quality = ffi.new("DWORD*")
        err = self.sgfplib.SGFPM_GetImageQuality(self.fpm[0], width, height, img, quality)
        if err != 0:
            raise Exception("SGFPM_GetImageQuality error: {}".format(err))
        return quality[0]

    def match_fingerprints(self, fingerprint1, fingerprint2):
        template1 = self.get_template(fingerprint1)
        template2 = self.get_template(fingerprint2)

        return self.match_templates(template1, template2)

    def get_template(self, fingerprint):
        for template in fingerprint.templates:
            if template.format == self.input_format:
                return template.template
        return None
