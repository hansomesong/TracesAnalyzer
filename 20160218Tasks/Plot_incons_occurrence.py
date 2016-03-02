# -*- coding: utf-8 -*-
__author__ = 'yueli'

import matplotlib.pyplot as plt
from config.config import *
import numpy as np
import math
from collections import Counter



plt.grid(True)
output_MR = [0.21283706717736245, 1.8872048424146288, 0.026631158455392812, 1.2496894526397697, 0.2996879682624504, 0.23932675865556857, 0.053262316910785625, 0.15950401677798348, 0.09993765615258773, 0.23925602516697522, 1.6222371941439746, 34.365834946617106, 0.07496886713885491, 1.57422120972064, 78.37930996767182, 0.12509394545928978, 0.025031289111389236, 1.4631391822649795, 0.1859937082561896, 0.026560424966799466, 0.20000031250048828, 15.1467111667362, 0.9495014835960681, 0.149812734082397, 0.8499388280294188, 57.137026776604344, 0.10000015625024414, 0.15018773466833543, 1.2496131762342553, 0.17496902338909903, 0.2656042496679946, 0.12503144536163338, 0.1500002343753662, 0.15957475026657683, 0.049937578027465665, 0.05000007812512207, 0.10006265634790054, 1.0572361387998037, 0.12496894526397698, 0.07496886713885491, 0.20000031250048828, 0.25006289072326676, 0.10000015625024414, 1.274720741751159, 1.1964923263006562, 0.14993773427770982, 0.9375, 0.12496894526397698, 0.19987531230517547, 0.14993773427770982, 0.6745948040543813, 0.15000023437536622, 1.499377342777098, 0.09987515605493133, 0.5998759373061521, 1.2495019523468005, 0.624719726124572, 0.07496886713885491, 36.639310489953196, 0.15950401677798348, 0.07130124777183601, 0.20006281259814468, 0.12490644516632057, 0.3455684585227664, 99.92503113286114, 0.12496894526397698, 0.6380868006005272, 1.7545441845578185, 1.3747833980990596, 0.3749068357919309, 0.12503144536163338, 0.049937578027465665, 0.053262316910785625, 0.31907876704456034, 0.5249695702649536, 0.07496886713885491, 1.25, 0.024968789013732832, 0.024968789013732832, 0.29993796865307604, 0.09993765615258773, 0.23918529167838187, 1.0994392178737782, 0.15012523457067903, 0.4253204669117582, 99.92503113286115, 1.1432300093898706, 1.3561378100558263, 0.15000023437536622, 0.9747202730004266, 0.09993765615258773, 0.07982274187758509, 0.22509410170953395, 99.90012484394506, 0.29258907556635416, 1.089543291547525, 0.026631158455392812, 0.14993773427770982, 0.08534850640113797, 0.15000023437536622, 1.568550476301629, 0.29251834207776084, 4.5736981059340085, 0.024968789013732832, 1.6993151551799301, 0.22478160122125193, 1.17021483528823, 0.05006257822277847]
output_VP = [0.08172438451322914, 0.7661661048115231, 0.010215548064153642, 0.5185825410544512, 0.12484394506866416, 0.1736643170906119, 0.020431096128307284, 1.6549187863928898, 0.03841352155958898, 0.09193993257738277, 0.6537950761058331, 31.61432824354172, 0.09603380389897244, 0.633823105733218, 31.210986267166046, 0.04801690194948622, 0.0864304235090752, 0.6556609296335323, 0.07150883644907549, 0.010215548064153642, 0.07682704311917794, 14.760395659272067, 0.40334197637568425, 0.05762028233938346, 0.6146163449534235, 0.3265149332565063, 65.97522327859407, 33.81346409234855, 0.24008450974743106, 0.5925017877209112, 0.7970805723614712, 0.10215548064153641, 0.12484394506866417, 0.05762028233938346, 0.061293288384921846, 0.01920676077979449, 0.09603380389897244, 0.11524056467876694, 0.09223390518354548, 0.27849803130702006, 0.028810141169691734, 0.07682704311917796, 0.09603380389897244, 0.03841352155958898, 0.11524056467876694, 0.5377893018342457, 0.48013075901522123, 0.48977239988475935, 0.5408653846153846, 0.04801690194948622, 0.07682704311917794, 0.1920676077979449, 0.2592912705272256, 0.44175549793527313, 0.7298569096321905, 0.1824642274080476, 0.2592912705272256, 0.508979160664554, 0.25929127052722556, 0.6146163449534234, 0.03841352155958898, 0.061293288384921846, 0.07682704311917796, 0.12484394506866418, 0.14301767289815095, 0.355325074426198, 0.12484394506866418, 0.25538870160384103, 0.7559505567473696, 0.5281859214443483, 0.16325746662825316, 0.04801690194948622, 0.01920676077979449, 0.07150883644907549, 0.12258657676984369, 0.2208777489676366, 0.03841352155958898, 0.42735042735042733, 0.009603380389897245, 0.009603380389897245, 0.11524056467876694, 0.03841352155958898, 0.09193993257738277, 0.030646644192460923, 0.4417554979352732, 0.05762028233938347, 0.18387986515476554, 21.492365312590035, 0.4596996628869139, 0.5720706915926039, 0.05762028233938347, 0.393738595985787, 0.26560424966799456, 0.03841352155958898, 0.11237102870569003, 0.0864304235090752, 0.17286084701815044, 0.11237102870569003, 0.6640106241699868, 0.4188374706302993, 0.05107774032076821, 0.05762028233938346, 0.03273322422258593, 0.07682704311917796, 4.310961283072836, 0.11237102870569006, 1.8387986515476553, 0.009603380389897245, 0.6626332469029099, 0.0864304235090752, 0.4596996628869139, 0.01920676077979449, 0.15365408623835589]


###################################### MR part ######################################
# 将 output 向上取整
output_int_MR = [math.ceil(i) for i in output_MR]
# 统计 output_int 落入以 1% 为区间的个数
output_int_count_MR = sorted((dict(Counter(output_int_MR)).items()))

# Modify the size and dpi of picture, default size is (8,6), default dpi is 80
plt.gcf().set_size_inches(10,9)
# Define font
font_label = {
    'fontname'   : 'Times New Roman',
    'color'      : 'black',
    'fontsize'   : 70
       }


# # Plot pdf 部分
# x_axis =  [i[0] for i in sorted((dict(Counter(output_int_MR)).items()))]
# x_axis.insert(0, 0.0)
# y_axis_pdf =  [i[1]/613.0*100 for i in sorted((dict(Counter(output_int_MR)).items()))]
# y_axis_pdf.insert(0, (613-len(output_int_MR))/613.0*100)
# print "Consistency by MR:", (613-len(output_int_MR))/613.0*100
#
# plt.scatter(x_axis, y_axis_pdf, c='black', s=100)
# plt.plot(x_axis, y_axis_pdf, c='black', linewidth=3)
# plt.xlim(0, 100)
# plt.ylim(-5, 90)
# plt.xlabel("inconsistent occurrence by MR (%)", fontsize=45, fontname='Times New Roman')
# plt.ylabel("pdf (%)", fontsize=45, fontname='Times New Roman')
# plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'pdf_incons_occur_MR.eps'), dpi=300, transparent=True)
# plt.show()


# Plot cdf 部分
x_axis =  [i[0] for i in sorted((dict(Counter(output_int_MR)).items()))]
x_axis.insert(0, 0.0)
y_axis_pdf =  [i[1]/613.0*100 for i in sorted((dict(Counter(output_int_MR)).items()))]
y_axis_pdf.insert(0, (613-len(output_int_MR))/613.0*100)

y_axis_cdf = []
for i in y_axis_pdf:
    if not y_axis_cdf:
        y_axis_cdf.append(i)
    else:
        y_axis_cdf.append(i + y_axis_cdf[-1])

print "y_axis_pdf:", y_axis_pdf
print "y_axis_cdf:", y_axis_cdf

plt.scatter(x_axis, y_axis_cdf, c='black', s=200)
plt.plot(x_axis, y_axis_cdf, c='black', linewidth=5)
plt.xlim(-0.3, 100)
plt.ylim(80, 100.05)
plt.xlabel("inconsistent occurrence by MR (%)", fontsize=45, fontname='Times New Roman')
plt.ylabel("cdf (%)", fontsize=45, fontname='Times New Roman')
plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'cdf_incons_occur_MR.eps'), dpi=300, transparent=True)
plt.show()



# ###################################### VP part ######################################
# # 将 output 向上取整
# output_int_VP = [math.ceil(i) for i in output_VP]
# # 统计 output_int 落入以 1% 为区间的个数
# output_int_count_VP = sorted((dict(Counter(output_int_VP)).items()))
#
# # Modify the size and dpi of picture, default size is (8,6), default dpi is 80
# plt.gcf().set_size_inches(10,9)
# # Define font
# font_label = {
#     'fontname'   : 'Times New Roman',
#     'color'      : 'black',
#     'fontsize'   : 70
#        }
#
#
# # # Plot pdf 部分
# # x_axis =  [i[0] for i in sorted((dict(Counter(output_int_VP)).items()))]
# # x_axis.insert(0, 0.0)
# # y_axis_pdf =  [i[1]/613.0*100 for i in sorted((dict(Counter(output_int_VP)).items()))]
# # y_axis_pdf.insert(0, (613-len(output_int_VP))/613.0*100)
# # print "Consistency by VP:", (613-len(output_int_VP))/613.0*100
# #
# # plt.scatter(x_axis, y_axis_pdf, c='black', s=100)
# # plt.plot(x_axis, y_axis_pdf, c='black', linewidth=3)
# # plt.xlim(0, 100)
# # plt.ylim(-5, 90)
# # plt.xlabel("inconsistent occurrence by VP(%)", fontsize=45, fontname='Times New Roman')
# # plt.ylabel("pdf (%)", fontsize=45, fontname='Times New Roman')
# # plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'pdf_incons_occur_VP.eps'), dpi=300, transparent=True)
# # plt.show()
#
#
# # Plot cdf 部分
# x_axis =  [i[0] for i in sorted((dict(Counter(output_int_VP)).items()))]
# x_axis.insert(0, 0.0)
# y_axis_pdf =  [i[1]/613.0*100 for i in sorted((dict(Counter(output_int_VP)).items()))]
# y_axis_pdf.insert(0, (613-len(output_int_VP))/613.0*100)
#
# y_axis_cdf = []
# for i in y_axis_pdf:
#     if not y_axis_cdf:
#         y_axis_cdf.append(i)
#     else:
#         y_axis_cdf.append(i + y_axis_cdf[-1])
#
# print "y_axis_pdf:", y_axis_pdf
# print "y_axis_cdf:", y_axis_cdf
#
# plt.scatter(x_axis, y_axis_cdf, c='black', s=200)
# plt.plot(x_axis, y_axis_cdf, c='black', linewidth=5)
# plt.xlim(-0.3, 100)
# plt.ylim(80, 100.05)
# plt.xlabel("inconsistent occurrence by VP (%)", fontsize=45, fontname='Times New Roman')
# plt.ylabel("cdf (%)", fontsize=45, fontname='Times New Roman')
# plt.savefig(os.path.join(PLOT_DIR, 'Plot_newSize', 'cdf_incons_occur_VP.eps'), dpi=300, transparent=True)
# plt.show()