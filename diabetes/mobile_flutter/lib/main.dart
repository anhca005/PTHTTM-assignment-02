import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(const DiabetesApp());

class DiabetesApp extends StatefulWidget {
  const DiabetesApp({super.key});

  @override
  State<DiabetesApp> createState() => _DiabetesAppState();
}

class _DiabetesAppState extends State<DiabetesApp> {
  bool isDarkMode = true;
  String lang = 'vi'; // 'vi' or 'en'

  void toggleTheme() => setState(() => isDarkMode = !isDarkMode);
  void toggleLang() => setState(() => lang = lang == 'vi' ? 'en' : 'vi');

  @override
  Widget build(BuildContext context) {
    final primaryColor = isDarkMode ? const Color(0xFF0EA5E9) : const Color(0xFF0284C7);
    final bgColor = isDarkMode ? const Color(0xFF090D16) : const Color(0xFFF1F5F9);
    final cardColor = isDarkMode ? const Color(0xFF1E293B) : Colors.white;
    final borderColor = isDarkMode ? const Color(0xFF334155) : const Color(0xFFE2E8F0);

    return MaterialApp(
      title: 'Diabetes Risk AI',
      debugShowCheckedModeBanner: false,
      themeMode: isDarkMode ? ThemeMode.dark : ThemeMode.light,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.light,
        colorScheme: ColorScheme.fromSeed(
          seedColor: primaryColor,
          brightness: Brightness.light,
          surface: cardColor,
        ),
        scaffoldBackgroundColor: bgColor,
        cardTheme: CardThemeData(
          color: cardColor,
          elevation: 2,
          shadowColor: Colors.black.withOpacity(0.05),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: BorderSide(color: borderColor, width: 1),
          ),
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: primaryColor,
          brightness: Brightness.dark,
          surface: cardColor,
        ),
        scaffoldBackgroundColor: bgColor,
        cardTheme: CardThemeData(
          color: cardColor,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: BorderSide(color: borderColor, width: 1),
          ),
        ),
      ),
      home: DiabetesPredictScreen(
        isDarkMode: isDarkMode,
        lang: lang,
        onToggleTheme: toggleTheme,
        onToggleLang: toggleLang,
      ),
    );
  }
}

class DiabetesPredictScreen extends StatefulWidget {
  final bool isDarkMode;
  final String lang;
  final VoidCallback onToggleTheme;
  final VoidCallback onToggleLang;

  const DiabetesPredictScreen({
    super.key,
    required this.isDarkMode,
    required this.lang,
    required this.onToggleTheme,
    required this.onToggleLang,
  });

  @override
  State<DiabetesPredictScreen> createState() => _DiabetesPredictScreenState();
}

class _DiabetesPredictScreenState extends State<DiabetesPredictScreen> {
  final apiUrlCtrl = TextEditingController(text: 'https://diabetes-api-q1ke.onrender.com');
  final ageCtrl = TextEditingController(text: '45');
  final bmiCtrl = TextEditingController(text: '24.5');
  final hba1cCtrl = TextEditingController(text: '5.7');
  final glucoseCtrl = TextEditingController(text: '120');

  String gender = 'Female';
  int hypertension = 0;
  int heartDisease = 0;
  String smokingHistory = 'never';

  bool loading = false;
  String? resultTitle;
  double? confidence;
  bool? isRisk;
  String rawJson = '';

  final List<String> smokingOptions = [
    'never',
    'No Info',
    'current',
    'former',
    'ever',
    'not current',
  ];

  String tr(String keyVi, String keyEn) {
    return widget.lang == 'vi' ? keyVi : keyEn;
  }

  Future<void> predict() async {
    FocusScope.of(context).unfocus();
    setState(() {
      loading = true;
      resultTitle = null;
    });

    try {
      final base = apiUrlCtrl.text.trim().replaceAll(RegExp(r'/+$'), '');
      final res = await http
          .post(
            Uri.parse('$base/predict'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'gender': gender,
              'age': double.tryParse(ageCtrl.text) ?? 0,
              'hypertension': hypertension,
              'heart_disease': heartDisease,
              'smoking_history': smokingHistory,
              'bmi': double.tryParse(bmiCtrl.text) ?? 0,
              'HbA1c_level': double.tryParse(hba1cCtrl.text) ?? 0,
              'blood_glucose_level': double.tryParse(glucoseCtrl.text) ?? 0,
            }),
          )
          .timeout(const Duration(seconds: 15));

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        final risk = data['prediction_label'] == 1;
        setState(() {
          isRisk = risk;
          resultTitle = data['prediction'] ?? (risk 
              ? tr('Có nguy cơ tiểu đường', 'High Diabetes Risk Detected') 
              : tr('Không mắc tiểu đường', 'No Diabetes Detected'));
          confidence = (data['confidence'] as num?)?.toDouble() ?? 0.0;
          rawJson = const JsonEncoder.withIndent('  ').convert(data);
        });
      } else {
        _showErrorSnackBar(tr('Lỗi Server (HTTP ${res.statusCode})', 'Server Error (HTTP ${res.statusCode})'));
      }
    } catch (e) {
      _showErrorSnackBar(tr('Lỗi kết nối API: $e', 'API Connection Error: $e'));
    } finally {
      setState(() {
        loading = false;
      });
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

  String _getBmiCategory(double bmi) {
    if (bmi <= 0) return '';
    if (bmi < 18.5) return tr('Gầy (< 18.5)', 'Underweight (< 18.5)');
    if (bmi < 24.9) return tr('Bình thường (18.5 - 24.9)', 'Normal (18.5 - 24.9)');
    if (bmi < 29.9) return tr('Thừa cân (25 - 29.9)', 'Overweight (25 - 29.9)');
    return tr('Béo phì (≥ 30)', 'Obese (≥ 30)');
  }

  Color _getBmiColor(double bmi) {
    if (bmi < 18.5) return const Color(0xFF0EA5E9);
    if (bmi < 24.9) return const Color(0xFF10B981);
    if (bmi < 29.9) return const Color(0xFFF59E0B);
    return const Color(0xFFEF4444);
  }

  @override
  Widget build(BuildContext context) {
    final currentBmi = double.tryParse(bmiCtrl.text) ?? 0;
    final isDark = widget.isDarkMode;
    final inputBg = isDark ? const Color(0xFF0F172A) : const Color(0xFFF8FAFC);
    final primaryHex = isDark ? const Color(0xFF0EA5E9) : const Color(0xFF0284C7);

    return Scaffold(
      appBar: AppBar(
        backgroundColor: isDark ? const Color(0xFF0F172A) : Colors.white,
        elevation: 0,
        scrolledUnderElevation: 1,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: primaryHex.withOpacity(0.15),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Icon(Icons.health_and_safety, color: primaryHex),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Diabetes Risk AI',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                Text(
                  tr('Dự đoán nguy cơ tiểu đường', 'Diabetes Risk Assessment'),
                  style: TextStyle(fontSize: 11, color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B)),
                ),
              ],
            ),
          ],
        ),
        actions: [
          // Theme Switcher Button
          IconButton(
            onPressed: widget.onToggleTheme,
            icon: Icon(isDark ? Icons.light_mode : Icons.dark_mode, size: 20),
            tooltip: isDark ? 'Chuyển Chế độ Sáng' : 'Chuyển Chế độ Tối',
          ),
          // Language Switcher Button
          Padding(
            padding: const EdgeInsets.only(right: 12),
            child: ActionChip(
              avatar: Text(widget.lang == 'vi' ? '🇻🇳' : '🇬🇧', style: const TextStyle(fontSize: 14)),
              label: Text(widget.lang.toUpperCase(), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
              backgroundColor: isDark ? const Color(0xFF1E293B) : const Color(0xFFF1F5F9),
              side: BorderSide(color: isDark ? const Color(0xFF334155) : const Color(0xFFCBD5E1)),
              onPressed: widget.onToggleLang,
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
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
                        Icon(Icons.dns, size: 18, color: primaryHex),
                        const SizedBox(width: 8),
                        Text(
                          tr('Cấu hình Kết nối API', 'API Connection Settings'),
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: primaryHex),
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
                        fillColor: inputBg,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 14),

            // Section 1: Thông tin cá nhân
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.person, size: 18, color: primaryHex),
                        const SizedBox(width: 8),
                        Text(tr('1. Thông tin cá nhân', '1. Personal Information'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      ],
                    ),
                    const SizedBox(height: 14),

                    // Gender Selector
                    Text(tr('Giới tính', 'Gender'), style: TextStyle(fontSize: 12, color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B))),
                    const SizedBox(height: 6),
                    SegmentedButton<String>(
                      segments: [
                        ButtonSegment(value: 'Female', label: Text(tr('Nữ', 'Female')), icon: const Icon(Icons.female, size: 18)),
                        ButtonSegment(value: 'Male', label: Text(tr('Nam', 'Male')), icon: const Icon(Icons.male, size: 18)),
                        ButtonSegment(value: 'Other', label: Text(tr('Khác', 'Other')), icon: const Icon(Icons.transgender, size: 18)),
                      ],
                      selected: {gender},
                      onSelectionChanged: (set) => setState(() => gender = set.first),
                      style: SegmentedButton.styleFrom(
                        selectedBackgroundColor: primaryHex,
                        selectedForegroundColor: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 14),

                    // Age input
                    TextField(
                      controller: ageCtrl,
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: tr('Tuổi (Age)', 'Age'),
                        prefixIcon: const Icon(Icons.cake, size: 20),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        isDense: true,
                        filled: true,
                        fillColor: inputBg,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 14),

            // Section 2: Tiền sử y tế
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.medical_services, size: 18, color: primaryHex),
                        const SizedBox(width: 8),
                        Text(tr('2. Tiền sử Y tế & Thói quen', '2. Medical History & Habits'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      ],
                    ),
                    const SizedBox(height: 12),

                    // Hypertension & Heart disease Switches
                    SwitchListTile(
                      title: Text(tr('Tăng huyết áp (Hypertension)', 'Hypertension'), style: const TextStyle(fontSize: 14)),
                      subtitle: Text(hypertension == 1 ? tr('Có tiền sử cao huyết áp', 'Has hypertension history') : tr('Không có', 'None'), style: TextStyle(fontSize: 12, color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B))),
                      value: hypertension == 1,
                      activeColor: const Color(0xFFEF4444),
                      onChanged: (val) => setState(() => hypertension = val ? 1 : 0),
                      contentPadding: EdgeInsets.zero,
                    ),
                    Divider(color: isDark ? const Color(0xFF334155) : const Color(0xFFE2E8F0)),
                    SwitchListTile(
                      title: Text(tr('Bệnh tim mạch (Heart Disease)', 'Heart Disease'), style: const TextStyle(fontSize: 14)),
                      subtitle: Text(heartDisease == 1 ? tr('Có tiền sử bệnh tim', 'Has heart disease history') : tr('Không có', 'None'), style: TextStyle(fontSize: 12, color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B))),
                      value: heartDisease == 1,
                      activeColor: const Color(0xFFEF4444),
                      onChanged: (val) => setState(() => heartDisease = val ? 1 : 0),
                      contentPadding: EdgeInsets.zero,
                    ),
                    const SizedBox(height: 10),

                    // Smoking History Chips
                    Text(tr('Tiền sử hút thuốc', 'Smoking History'), style: TextStyle(fontSize: 12, color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B))),
                    const SizedBox(height: 8),
                    Wrap(
                      spacing: 8,
                      runSpacing: 6,
                      children: smokingOptions.map((opt) {
                        final isSel = smokingHistory == opt;
                        return ChoiceChip(
                          label: Text(opt),
                          selected: isSel,
                          selectedColor: primaryHex,
                          onSelected: (sel) {
                            if (sel) setState(() => smokingHistory = opt);
                          },
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 14),

            // Section 3: Chỉ số Sinh hiệu / Xét nghiệm
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.monitor_weight, size: 18, color: primaryHex),
                        const SizedBox(width: 8),
                        Text(tr('3. Chỉ số Xét nghiệm & Thân hình', '3. Biomarkers & Physical Metrics'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      ],
                    ),
                    const SizedBox(height: 14),

                    // BMI
                    TextField(
                      controller: bmiCtrl,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      onChanged: (_) => setState(() {}),
                      decoration: InputDecoration(
                        labelText: tr('Chỉ số BMI (kg/m²)', 'BMI Index (kg/m²)'),
                        prefixIcon: const Icon(Icons.straighten, size: 20),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        isDense: true,
                        filled: true,
                        fillColor: inputBg,
                        suffixIcon: currentBmi > 0
                            ? Padding(
                                padding: const EdgeInsets.only(right: 8),
                                child: Chip(
                                  label: Text(
                                    _getBmiCategory(currentBmi),
                                    style: const TextStyle(fontSize: 10, color: Colors.white, fontWeight: FontWeight.bold),
                                  ),
                                  backgroundColor: _getBmiColor(currentBmi).withOpacity(0.85),
                                  padding: EdgeInsets.zero,
                                  visualDensity: VisualDensity.compact,
                                ),
                              )
                            : null,
                      ),
                    ),
                    const SizedBox(height: 12),

                    // HbA1c
                    TextField(
                      controller: hba1cCtrl,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      decoration: InputDecoration(
                        labelText: tr('Chỉ số HbA1c (%) — Chuẩn < 5.7%', 'HbA1c level (%) — Normal < 5.7%'),
                        prefixIcon: const Icon(Icons.science, size: 20),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        isDense: true,
                        filled: true,
                        fillColor: inputBg,
                      ),
                    ),
                    const SizedBox(height: 12),

                    // Blood Glucose
                    TextField(
                      controller: glucoseCtrl,
                      keyboardType: TextInputType.number,
                      decoration: InputDecoration(
                        labelText: tr('Đường huyết lúc đói (mg/dL) — Chuẩn < 140', 'Blood Glucose level (mg/dL) — Normal < 140'),
                        prefixIcon: const Icon(Icons.opacity, size: 20),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        isDense: true,
                        filled: true,
                        fillColor: inputBg,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Predict Button
            Container(
              height: 52,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(14),
                gradient: LinearGradient(
                  colors: [primaryHex, const Color(0xFF2563EB)],
                ),
                boxShadow: [
                  BoxShadow(
                    color: primaryHex.withOpacity(0.35),
                    blurRadius: 12,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: ElevatedButton(
                onPressed: loading ? null : predict,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.transparent,
                  shadowColor: Colors.transparent,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                ),
                child: loading
                    ? const SizedBox(
                        height: 24,
                        width: 24,
                        child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5),
                      )
                    : Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.analytics, color: Colors.white),
                          const SizedBox(width: 8),
                          Text(
                            tr('Phân Tích Nguy Cơ AI', 'Analyze Risk with AI'),
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white),
                          ),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 24),

            // Result Display
            if (resultTitle != null) ...[
              Card(
                color: isRisk == true 
                    ? (isDark ? const Color(0xFF451A1A) : const Color(0xFFFEF2F2))
                    : (isDark ? const Color(0xFF064E3B) : const Color(0xFFECFDF5)),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: BorderSide(
                    color: isRisk == true ? const Color(0xFFEF4444) : const Color(0xFF10B981),
                    width: 1.5,
                  ),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      Icon(
                        isRisk == true ? Icons.warning_amber_rounded : Icons.check_circle_outline,
                        size: 48,
                        color: isRisk == true ? const Color(0xFFEF4444) : const Color(0xFF10B981),
                      ),
                      const SizedBox(height: 10),
                      Text(
                        resultTitle!,
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                          color: isRisk == true ? const Color(0xFFEF4444) : const Color(0xFF10B981),
                        ),
                      ),
                      const SizedBox(height: 12),

                      if (confidence != null) ...[
                        Text(
                          tr('Độ tin cậy mô hình: ${(confidence! * 100).toStringAsFixed(1)}%', 'Model Confidence: ${(confidence! * 100).toStringAsFixed(1)}%'),
                          style: TextStyle(fontSize: 13, color: isDark ? const Color(0xFFE2E8F0) : const Color(0xFF334155)),
                        ),
                        const SizedBox(height: 8),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(10),
                          child: LinearProgressIndicator(
                            value: confidence,
                            minHeight: 8,
                            backgroundColor: Colors.black12,
                            color: isRisk == true ? const Color(0xFFEF4444) : const Color(0xFF10B981),
                          ),
                        ),
                      ],
                      const SizedBox(height: 16),
                      Text(
                        isRisk == true
                            ? tr('⚠️ Bạn có các chỉ số nằm trong nhóm nguy cơ cao. Hãy tham khảo ý kiến bác sĩ chuyên khoa.', '⚠️ Your metrics indicate high risk. Please consult a medical specialist for clinical diagnosis.')
                            : tr('✅ Các chỉ số hiện tại nằm trong giới hạn an toàn. Duy trì chế độ ăn uống & tập luyện lành mạnh.', '✅ Your metrics are within safe limits. Continue maintaining a healthy diet and lifestyle.'),
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 12, color: isDark ? const Color(0xFFCBD5E1) : const Color(0xFF475569)),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 14),

              // Expandable Raw Json
              ExpansionTile(
                title: Text(tr('Xem phản hồi JSON gốc', 'View Raw JSON Response'), style: TextStyle(fontSize: 13, color: isDark ? const Color(0xFF94A3B8) : const Color(0xFF64748B))),
                children: [
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: inputBg,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      rawJson,
                      style: TextStyle(fontFamily: 'monospace', fontSize: 11, color: primaryHex),
                    ),
                  ),
                ],
              ),
            ],
          ],
        ),
      ),
    );
  }
}
