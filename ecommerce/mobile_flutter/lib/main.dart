import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(const EcommerceApp());

class EcommerceApp extends StatelessWidget {
  const EcommerceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'E-Commerce Recommendation AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF8B5CF6),
          brightness: Brightness.dark,
          surface: const Color(0xFF0F172A),
        ),
        scaffoldBackgroundColor: const Color(0xFF090D16),
        cardTheme: CardTheme(
          color: const Color(0xFF1E293B),
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: const BorderSide(color: Color(0xFF334155), width: 1),
          ),
        ),
      ),
      home: const EcommercePredictScreen(),
    );
  }
}

const divisions = ['General', 'General Petite', 'Initmates'];
const departments = ['Dresses', 'Tops', 'Bottoms', 'Intimate', 'Jackets', 'Trend'];
const classes = [
  'Dresses', 'Knits', 'Blouses', 'Sweaters', 'Pants', 'Jeans', 'Fine gauge',
  'Skirts', 'Jackets', 'Lounge', 'Swim', 'Outerwear', 'Shorts', 'Sleep',
  'Legwear', 'Intimates', 'Layering', 'Trend', 'Casual bottoms', 'Chemises',
];

class EcommercePredictScreen extends StatefulWidget {
  const EcommercePredictScreen({super.key});

  @override
  State<EcommercePredictScreen> createState() => _EcommercePredictScreenState();
}

class _EcommercePredictScreenState extends State<EcommercePredictScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  String lang = 'vi'; // 'vi' or 'en'

  final apiUrlCtrl = TextEditingController(text: 'http://192.168.1.10:8002');

  // Tab 1 Controllers & State
  final ageCtrl = TextEditingController(text: '35');
  final feedbackCtrl = TextEditingController(text: '2');
  final titleCtrl = TextEditingController(text: 'Great fit');
  final reviewCtrl = TextEditingController(text: 'Absolutely love this dress, fits perfectly and so comfortable!');
  int rating = 5;
  String division = 'General';
  String department = 'Dresses';
  String klass = 'Dresses';

  bool loadingTab1 = false;
  String? resultTextTab1;
  bool? isRecommendedTab1;
  double? probTab1;
  String rawJsonTab1 = '';

  // Tab 2 Controllers & State
  final freeTextCtrl = TextEditingController(text: 'This runs small and the fabric feels cheap, I would not buy again.');
  bool loadingTab2 = false;
  String? resultTextTab2;
  bool? isRecommendedTab2;
  double? probTab2;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  String tr(String keyVi, String keyEn) {
    return lang == 'vi' ? keyVi : keyEn;
  }

  Future<void> predictStructured() async {
    FocusScope.of(context).unfocus();
    setState(() {
      loadingTab1 = true;
      resultTextTab1 = null;
    });

    try {
      final base = apiUrlCtrl.text.trim().replaceAll(RegExp(r'/+$'), '');
      final res = await http
          .post(
            Uri.parse('$base/predict'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'Age': double.tryParse(ageCtrl.text) ?? 0,
              'Rating': rating,
              'Positive Feedback Count': int.tryParse(feedbackCtrl.text) ?? 0,
              'Review Text': reviewCtrl.text,
              'Title': titleCtrl.text,
              'Division Name': division,
              'Department Name': department,
              'Class Name': klass,
            }),
          )
          .timeout(const Duration(seconds: 15));

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        final rec = data['prediction_label'] == 1;
        setState(() {
          isRecommendedTab1 = rec;
          probTab1 = (data['probability_recommended'] as num?)?.toDouble() ?? 0.0;
          resultTextTab1 = data['prediction'] ?? (rec ? tr('Khuyên dùng', 'Recommended') : tr('Không khuyên dùng', 'Not Recommended'));
          rawJsonTab1 = const JsonEncoder.withIndent('  ').convert(data);
        });
      } else {
        _showErrorSnackBar(tr('Lỗi Server (HTTP ${res.statusCode})', 'Server Error (HTTP ${res.statusCode})'));
      }
    } catch (e) {
      _showErrorSnackBar(tr('Lỗi kết nối API: $e', 'API Connection Error: $e'));
    } finally {
      setState(() => loadingTab1 = false);
    }
  }

  Future<void> analyzeFreeText() async {
    FocusScope.of(context).unfocus();
    setState(() {
      loadingTab2 = true;
      resultTextTab2 = null;
    });

    try {
      final base = apiUrlCtrl.text.trim().replaceAll(RegExp(r'/+$'), '');
      final res = await http
          .post(
            Uri.parse('$base/analyze_text'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'text': freeTextCtrl.text}),
          )
          .timeout(const Duration(seconds: 15));

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        final rec = data['prediction'] == 'Recommended';
        setState(() {
          isRecommendedTab2 = rec;
          probTab2 = (data['probability_recommended'] as num?)?.toDouble() ?? 0.0;
          resultTextTab2 = data['prediction'];
        });
      } else {
        _showErrorSnackBar(tr('Lỗi Server (HTTP ${res.statusCode})', 'Server Error (HTTP ${res.statusCode})'));
      }
    } catch (e) {
      _showErrorSnackBar(tr('Lỗi kết nối API: $e', 'API Connection Error: $e'));
    } finally {
      setState(() => loadingTab2 = false);
    }
  }

  void _showErrorSnackBar(String msg) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg),
        backgroundColor: const Color(0xFFEF4444),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  void _fillPositivePreset() {
    setState(() {
      rating = 5;
      titleCtrl.text = lang == 'vi' ? 'Tuyệt vời ngoài mong đợi!' : 'Exceeded Expectations!';
      reviewCtrl.text = lang == 'vi' 
          ? 'Chất vải mềm mịn, tôn dáng và mặc rất thoải mái. Rất đáng tiền!' 
          : 'Great quality fabric, very flattering fit and super comfortable. Highly recommended!';
    });
  }

  void _fillNegativePreset() {
    setState(() {
      rating = 1;
      titleCtrl.text = lang == 'vi' ? 'Rất thất vọng' : 'Very Disappointed';
      reviewCtrl.text = lang == 'vi' 
          ? 'Kích thước quá nhỏ so với mô tả, vải mỏng chỉ dùng làm giẻ lau được.' 
          : 'Runs extremely small, cheap fabric quality. Would not buy again.';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0F172A),
        elevation: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: const Color(0xFF8B5CF6).withOpacity(0.2),
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Icon(Icons.shopping_bag, color: Color(0xFF8B5CF6)),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Recommend Check AI',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                Text(
                  tr('Dự đoán đề xuất & Phân tích Cảm xúc', 'Recommendation & Sentiment AI'),
                  style: const TextStyle(fontSize: 11, color: Color(0xFF94A3B8)),
                ),
              ],
            ),
          ],
        ),
        actions: [
          // Language Switcher Button
          Padding(
            padding: const EdgeInsets.only(right: 12),
            child: ActionChip(
              avatar: Text(lang == 'vi' ? '🇻🇳' : '🇬🇧', style: const TextStyle(fontSize: 14)),
              label: Text(lang.toUpperCase(), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
              backgroundColor: const Color(0xFF1E293B),
              side: const BorderSide(color: Color(0xFF334155)),
              onPressed: () {
                setState(() {
                  lang = lang == 'vi' ? 'en' : 'vi';
                });
              },
            ),
          ),
        ],
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: const Color(0xFF8B5CF6),
          labelColor: const Color(0xFF8B5CF6),
          unselectedLabelColor: const Color(0xFF94A3B8),
          tabs: [
            Tab(icon: const Icon(Icons.rate_review_outlined, size: 20), text: tr('1. Đánh Giá Cấu Trúc', '1. Tabular Review')),
            Tab(icon: const Icon(Icons.psychology, size: 20), text: tr('2. Phân Tích NLP / Text', '2. NLP Text Model')),
          ],
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // API Server Config Card
            Card(
              child: Padding(
                padding: const EdgeInsets.all(14),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.dns, size: 18, color: Color(0xFF8B5CF6)),
                        const SizedBox(width: 8),
                        Text(
                          tr('Cấu hình Kết nối Server API', 'API Connection Settings'),
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFF8B5CF6)),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    TextField(
                      controller: apiUrlCtrl,
                      decoration: InputDecoration(
                        labelText: 'API Base URL',
                        prefixIcon: const Icon(Icons.link, size: 20),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        isDense: true,
                        filled: true,
                        fillColor: const Color(0xFF0F172A),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            SizedBox(
              height: 780,
              child: TabBarView(
                controller: _tabController,
                children: [
                  // TAB 1: Structured Review Form
                  SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Text(tr('Điền mẫu thử nhanh:', 'Quick sample presets:'), style: const TextStyle(fontSize: 12, color: Color(0xFF94A3B8))),
                                    Row(
                                      children: [
                                        TextButton.icon(
                                          onPressed: _fillPositivePreset,
                                          icon: const Icon(Icons.thumb_up, size: 14, color: Color(0xFF10B981)),
                                          label: Text(tr('Mẫu 5⭐', 'Preset 5⭐'), style: const TextStyle(fontSize: 12, color: Color(0xFF10B981))),
                                        ),
                                        TextButton.icon(
                                          onPressed: _fillNegativePreset,
                                          icon: const Icon(Icons.thumb_down, size: 14, color: Color(0xFFEF4444)),
                                          label: Text(tr('Mẫu 1⭐', 'Preset 1⭐'), style: const TextStyle(fontSize: 12, color: Color(0xFFEF4444))),
                                        ),
                                      ],
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 10),

                                // Rating bar
                                Text(tr('Đánh giá Số Sao (Rating)', 'Star Rating'), style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
                                const SizedBox(height: 6),
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: List.generate(5, (index) {
                                    final starVal = index + 1;
                                    return IconButton(
                                      onPressed: () => setState(() => rating = starVal),
                                      icon: Icon(
                                        starVal <= rating ? Icons.star_rounded : Icons.star_outline_rounded,
                                        color: Colors.amber,
                                        size: 32,
                                      ),
                                    );
                                  }),
                                ),
                                const SizedBox(height: 12),

                                Row(
                                  children: [
                                    Expanded(
                                      child: TextField(
                                        controller: ageCtrl,
                                        keyboardType: TextInputType.number,
                                        decoration: InputDecoration(
                                          labelText: tr('Tuổi khách hàng', 'Customer Age'),
                                          prefixIcon: const Icon(Icons.person, size: 20),
                                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                          isDense: true,
                                          filled: true,
                                          fillColor: const Color(0xFF0F172A),
                                        ),
                                      ),
                                    ),
                                    const SizedBox(width: 10),
                                    Expanded(
                                      child: TextField(
                                        controller: feedbackCtrl,
                                        keyboardType: TextInputType.number,
                                        decoration: InputDecoration(
                                          labelText: tr('Lượt Like (Feedback)', 'Positive Feedback Count'),
                                          prefixIcon: const Icon(Icons.thumb_up_alt, size: 20),
                                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                          isDense: true,
                                          filled: true,
                                          fillColor: const Color(0xFF0F172A),
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 12),

                                TextField(
                                  controller: titleCtrl,
                                  decoration: InputDecoration(
                                    labelText: tr('Tiêu đề Đánh giá', 'Review Title'),
                                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                    isDense: true,
                                    filled: true,
                                    fillColor: const Color(0xFF0F172A),
                                  ),
                                ),
                                const SizedBox(height: 12),

                                TextField(
                                  controller: reviewCtrl,
                                  maxLines: 3,
                                  decoration: InputDecoration(
                                    labelText: tr('Nội dung Đánh giá sản phẩm', 'Review Text'),
                                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                    filled: true,
                                    fillColor: const Color(0xFF0F172A),
                                  ),
                                ),
                                const SizedBox(height: 14),

                                // Categories Dropdowns
                                DropdownButtonFormField<String>(
                                  value: division,
                                  decoration: InputDecoration(
                                    labelText: tr('Phân vùng (Division)', 'Division Name'),
                                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                    isDense: true,
                                    filled: true,
                                    fillColor: const Color(0xFF0F172A),
                                  ),
                                  items: divisions.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
                                  onChanged: (v) => setState(() => division = v!),
                                ),
                                const SizedBox(height: 12),

                                Row(
                                  children: [
                                    Expanded(
                                      child: DropdownButtonFormField<String>(
                                        value: department,
                                        decoration: InputDecoration(
                                          labelText: tr('Bộ phận (Dept)', 'Department Name'),
                                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                          isDense: true,
                                          filled: true,
                                          fillColor: const Color(0xFF0F172A),
                                        ),
                                        items: departments.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
                                        onChanged: (v) => setState(() => department = v!),
                                      ),
                                    ),
                                    const SizedBox(width: 10),
                                    Expanded(
                                      child: DropdownButtonFormField<String>(
                                        value: klass,
                                        decoration: InputDecoration(
                                          labelText: tr('Loại (Class)', 'Product Class'),
                                          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                          isDense: true,
                                          filled: true,
                                          fillColor: const Color(0xFF0F172A),
                                        ),
                                        items: classes.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
                                        onChanged: (v) => setState(() => klass = v!),
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),

                        // Predict Button
                        Container(
                          height: 50,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(14),
                            gradient: const LinearGradient(
                              colors: [Color(0xFF8B5CF6), Color(0xFFEC4899)],
                            ),
                          ),
                          child: ElevatedButton(
                            onPressed: loadingTab1 ? null : predictStructured,
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.transparent,
                              shadowColor: Colors.transparent,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                            ),
                            child: loadingTab1
                                ? const SizedBox(
                                    height: 24,
                                    width: 24,
                                    child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5),
                                  )
                                : Text(
                                    tr('Dự Đoán Khả Năng Đề Xuất', 'Predict Recommendation'),
                                    style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                                  ),
                          ),
                        ),
                        const SizedBox(height: 16),

                        // Tab 1 Result
                        if (resultTextTab1 != null) ...[
                          Card(
                            color: isRecommendedTab1 == true ? const Color(0xFF064E3B) : const Color(0xFF451A1A),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16),
                              side: BorderSide(
                                color: isRecommendedTab1 == true ? const Color(0xFF10B981) : const Color(0xFFEF4444),
                                width: 1.5,
                              ),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(18),
                              child: Column(
                                children: [
                                  Icon(
                                    isRecommendedTab1 == true ? Icons.recommend : Icons.do_not_disturb_on,
                                    size: 42,
                                    color: isRecommendedTab1 == true ? const Color(0xFF34D399) : const Color(0xFFF87171),
                                  ),
                                  const SizedBox(height: 8),
                                  Text(
                                    resultTextTab1!,
                                    style: TextStyle(
                                      fontSize: 22,
                                      fontWeight: FontWeight.bold,
                                      color: isRecommendedTab1 == true ? const Color(0xFF34D399) : const Color(0xFFF87171),
                                    ),
                                  ),
                                  if (probTab1 != null) ...[
                                    const SizedBox(height: 6),
                                    Text(
                                      tr('Xác suất Đề xuất: ${(probTab1! * 100).toStringAsFixed(1)}%', 'Recommendation Probability: ${(probTab1! * 100).toStringAsFixed(1)}%'),
                                      style: const TextStyle(fontSize: 13, color: Color(0xFFE2E8F0)),
                                    ),
                                  ],
                                ],
                              ),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),

                  // TAB 2: NLP Text Analysis
                  SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    const Icon(Icons.auto_awesome, size: 18, color: Color(0xFFEC4899)),
                                    const SizedBox(width: 8),
                                    Text(tr('Phân tích Văn bản Tự do bằng AI NLP', 'Free Text Review NLP Sentiment Analysis'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                                  ],
                                ),
                                const SizedBox(height: 12),
                                TextField(
                                  controller: freeTextCtrl,
                                  maxLines: 5,
                                  decoration: InputDecoration(
                                    labelText: tr('Nhập bất kỳ đoạn đánh giá sản phẩm nào...', 'Enter any product review text...'),
                                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                                    filled: true,
                                    fillColor: const Color(0xFF0F172A),
                                  ),
                                ),
                                const SizedBox(height: 16),
                                Container(
                                  height: 48,
                                  width: double.infinity,
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(12),
                                    gradient: const LinearGradient(
                                      colors: [Color(0xFFEC4899), Color(0xFF8B5CF6)],
                                    ),
                                  ),
                                  child: ElevatedButton.icon(
                                    onPressed: loadingTab2 ? null : analyzeFreeText,
                                    icon: const Icon(Icons.psychology, color: Colors.white),
                                    label: loadingTab2
                                        ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                                        : Text(tr('Phân Tích Cảm Xúc & Đề Xuất AI', 'Analyze Sentiment with AI'), style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: Colors.transparent,
                                      shadowColor: Colors.transparent,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 16),

                        if (resultTextTab2 != null) ...[
                          Card(
                            color: isRecommendedTab2 == true ? const Color(0xFF064E3B) : const Color(0xFF451A1A),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(16),
                              side: BorderSide(
                                color: isRecommendedTab2 == true ? const Color(0xFF10B981) : const Color(0xFFEF4444),
                                width: 1.5,
                              ),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(18),
                              child: Column(
                                children: [
                                  Icon(
                                    isRecommendedTab2 == true ? Icons.sentiment_very_satisfied : Icons.sentiment_very_dissatisfied,
                                    size: 42,
                                    color: isRecommendedTab2 == true ? const Color(0xFF34D399) : const Color(0xFFF87171),
                                  ),
                                  const SizedBox(height: 8),
                                  Text(
                                    resultTextTab2!,
                                    style: TextStyle(
                                      fontSize: 22,
                                      fontWeight: FontWeight.bold,
                                      color: isRecommendedTab2 == true ? const Color(0xFF34D399) : const Color(0xFFF87171),
                                    ),
                                  ),
                                  if (probTab2 != null) ...[
                                    const SizedBox(height: 6),
                                    Text(
                                      tr('Tỷ lệ Đề xuất (Confidence): ${(probTab2! * 100).toStringAsFixed(1)}%', 'Recommendation Confidence: ${(probTab2! * 100).toStringAsFixed(1)}%'),
                                      style: const TextStyle(fontSize: 13, color: Color(0xFFE2E8F0)),
                                    ),
                                  ],
                                ],
                              ),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
