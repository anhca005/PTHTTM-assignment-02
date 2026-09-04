import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(const HousePriceApp());

class HousePriceApp extends StatelessWidget {
  const HousePriceApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Real Estate Valuation AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFF59E0B),
          brightness: Brightness.dark,
          surface: const Color(0xFF0F172A),
        ),
        scaffoldBackgroundColor: const Color(0xFF0B0F19),
        cardTheme: CardTheme(
          color: const Color(0xFF1E293B),
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
            side: const BorderSide(color: Color(0xFF334155), width: 1),
          ),
        ),
      ),
      home: const HousePricePredictScreen(),
    );
  }
}

const houseDirections = [
  'Unknown', 'Đông', 'Tây', 'Nam', 'Bắc',
  'Đông - Nam', 'Đông - Bắc', 'Tây - Nam', 'Tây - Bắc',
];

const provinces = [
  'Hà Nội', 'Hồ Chí Minh', 'Bình Dương', 'Đà Nẵng', 'Đồng Nai', 'Hải Phòng',
  'Khánh Hòa', 'Hưng Yên', 'Long An', 'Bà Rịa Vũng Tàu', 'Bắc Ninh',
  'Bình Thuận', 'Khac',
];

class HousePricePredictScreen extends StatefulWidget {
  const HousePricePredictScreen({super.key});

  @override
  State<HousePricePredictScreen> createState() => _HousePricePredictScreenState();
}

class _HousePricePredictScreenState extends State<HousePricePredictScreen> {
  String lang = 'vi'; // 'vi' or 'en'

  final apiUrlCtrl = TextEditingController(text: 'http://192.168.1.10:8001');
  final areaCtrl = TextEditingController(text: '60');
  final frontageCtrl = TextEditingController(text: '4.5');
  final accessRoadCtrl = TextEditingController(text: '6');

  int floors = 3;
  int bedrooms = 3;
  int bathrooms = 2;

  String legalStatus = 'Have certificate';
  String furnitureState = 'Full';
  String houseDirection = 'Unknown';
  String balconyDirection = 'Unknown';
  String province = 'Hà Nội';

  bool loading = false;
  String? predictedPrice;
  String? priceUnit;
  String? modelUsed;
  String rawJson = '';

  String tr(String keyVi, String keyEn) {
    return lang == 'vi' ? keyVi : keyEn;
  }

  Future<void> predict() async {
    FocusScope.of(context).unfocus();
    setState(() {
      loading = true;
      predictedPrice = null;
    });

    try {
      final base = apiUrlCtrl.text.trim().replaceAll(RegExp(r'/+$'), '');
      final res = await http
          .post(
            Uri.parse('$base/predict'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'Area': double.tryParse(areaCtrl.text) ?? 0,
              'Frontage': double.tryParse(frontageCtrl.text) ?? 0,
              'Access Road': double.tryParse(accessRoadCtrl.text) ?? 0,
              'Floors': floors.toDouble(),
              'Bedrooms': bedrooms.toDouble(),
              'Bathrooms': bathrooms.toDouble(),
              'Legal status': legalStatus,
              'Furniture state': furnitureState,
              'House direction': houseDirection,
              'Balcony direction': balconyDirection,
              'ProvinceGroup': province,
            }),
          )
          .timeout(const Duration(seconds: 15));

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        setState(() {
          predictedPrice = data['predicted_price']?.toString() ?? 'N/A';
          priceUnit = data['predicted_price_unit'] ?? '';
          modelUsed = data['model_used'] ?? 'AI Model';
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

  Widget _buildCounterTile({
    required String title,
    required IconData icon,
    required int value,
    required ValueChanged<int> onChanged,
  }) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Row(
          children: [
            Icon(icon, size: 18, color: const Color(0xFFF59E0B)),
            const SizedBox(width: 8),
            Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
          ],
        ),
        Row(
          children: [
            IconButton.filledTonal(
              onPressed: value > 0 ? () => onChanged(value - 1) : null,
              icon: const Icon(Icons.remove, size: 16),
              constraints: const BoxConstraints(minWidth: 32, minHeight: 32),
              padding: EdgeInsets.zero,
            ),
            SizedBox(
              width: 32,
              child: Text(
                '$value',
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
              ),
            ),
            IconButton.filledTonal(
              onPressed: () => onChanged(value + 1),
              icon: const Icon(Icons.add, size: 16),
              constraints: const BoxConstraints(minWidth: 32, minHeight: 32),
              padding: EdgeInsets.zero,
            ),
          ],
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final areaVal = double.tryParse(areaCtrl.text) ?? 0;

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0B0F19),
        elevation: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: const Color(0xFFF59E0B).withOpacity(0.2),
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Icon(Icons.home_work_rounded, color: Color(0xFFF59E0B)),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Real Estate AI Valuation',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                Text(
                  tr('Định giá Bất động sản AI', 'AI Property Valuation'),
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
                        const Icon(Icons.dns, size: 18, color: Color(0xFFF59E0B)),
                        const SizedBox(width: 8),
                        Text(
                          tr('Cấu hình Kết nối Server API', 'API Connection Settings'),
                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Color(0xFFF59E0B)),
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
            const SizedBox(height: 14),

            // Section 1: Vị trí & Pháp lý
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.location_on, size: 18, color: Color(0xFFF59E0B)),
                        const SizedBox(width: 8),
                        Text(tr('1. Vị trí & Pháp lý', '1. Location & Legal Status'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      ],
                    ),
                    const SizedBox(height: 14),

                    // Province Dropdown
                    DropdownButtonFormField<String>(
                      value: province,
                      decoration: InputDecoration(
                        labelText: tr('Tỉnh / Thành phố', 'Province / City'),
                        prefixIcon: const Icon(Icons.location_city, size: 20),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        isDense: true,
                        filled: true,
                        fillColor: const Color(0xFF0F172A),
                      ),
                      items: provinces.map((p) => DropdownMenuItem(value: p, child: Text(p))).toList(),
                      onChanged: (v) => setState(() => province = v!),
                    ),
                    const SizedBox(height: 14),

                    // Legal status Chips
                    Text(tr('Tình trạng pháp lý', 'Legal Status'), style: const TextStyle(fontSize: 12, color: Color(0xFF94A3B8))),
                    const SizedBox(height: 6),
                    Wrap(
                      spacing: 8,
                      children: ['Have certificate', 'Sale contract', 'Unknown'].map((opt) {
                        final labelMap = {
                          'Have certificate': tr('📜 Sổ đỏ / Sổ hồng', '📜 Title Deed / Certificate'),
                          'Sale contract': tr('📝 Hợp đồng mua bán', '📝 Sale Contract'),
                          'Unknown': tr('❓ Chưa xác định', '❓ Unknown / Other')
                        };
                        final isSel = legalStatus == opt;
                        return ChoiceChip(
                          label: Text(labelMap[opt]!),
                          selected: isSel,
                          selectedColor: const Color(0xFFF59E0B),
                          onSelected: (sel) {
                            if (sel) setState(() => legalStatus = opt);
                          },
                        );
                      }).toList(),
                    ),
                    const SizedBox(height: 12),

                    // Furniture State Chips
                    Text(tr('Tình trạng nội thất', 'Furniture Condition'), style: const TextStyle(fontSize: 12, color: Color(0xFF94A3B8))),
                    const SizedBox(height: 6),
                    Wrap(
                      spacing: 8,
                      children: ['Full', 'Basic', 'Unknown'].map((opt) {
                        final labelMap = {
                          'Full': tr('🛋️ Đầy đủ nội thất', '🛋️ Fully Furnished'),
                          'Basic': tr('🏠 Nội thất cơ bản', '🏠 Basic Furnished'),
                          'Unknown': tr('📦 Bàn giao thô / Khác', '📦 Unfurnished / Bare')
                        };
                        final isSel = furnitureState == opt;
                        return ChoiceChip(
                          label: Text(labelMap[opt]!),
                          selected: isSel,
                          selectedColor: const Color(0xFFF59E0B),
                          onSelected: (sel) {
                            if (sel) setState(() => furnitureState = opt);
                          },
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 14),

            // Section 2: Thông số Diện tích
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.square_foot, size: 18, color: Color(0xFFF59E0B)),
                        const SizedBox(width: 8),
                        Text(tr('2. Thông số Kích thước', '2. Dimensions & Road Width'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      ],
                    ),
                    const SizedBox(height: 14),

                    // Area
                    TextField(
                      controller: areaCtrl,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      onChanged: (_) => setState(() {}),
                      decoration: InputDecoration(
                        labelText: tr('Diện tích (m²)', 'Area (m²)'),
                        prefixIcon: const Icon(Icons.aspect_ratio, size: 20),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                        isDense: true,
                        filled: true,
                        fillColor: const Color(0xFF0F172A),
                      ),
                    ),
                    const SizedBox(height: 12),

                    Row(
                      children: [
                        Expanded(
                          child: TextField(
                            controller: frontageCtrl,
                            keyboardType: const TextInputType.numberWithOptions(decimal: true),
                            decoration: InputDecoration(
                              labelText: tr('Mặt tiền (m)', 'Frontage (m)'),
                              prefixIcon: const Icon(Icons.swap_horiz, size: 20),
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
                            controller: accessRoadCtrl,
                            keyboardType: const TextInputType.numberWithOptions(decimal: true),
                            decoration: InputDecoration(
                              labelText: tr('Đường vào (m)', 'Access Road (m)'),
                              prefixIcon: const Icon(Icons.add_road, size: 20),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                              isDense: true,
                              filled: true,
                              fillColor: const Color(0xFF0F172A),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 14),

            // Section 3: Quy mô & Hướng nhà
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.king_bed, size: 18, color: Color(0xFFF59E0B)),
                        const SizedBox(width: 8),
                        Text(tr('3. Quy mô & Hướng nhà', '3. Scale & Orientation'), style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      ],
                    ),
                    const SizedBox(height: 12),

                    _buildCounterTile(
                      title: tr('Số tầng (Floors)', 'Floors'),
                      icon: Icons.layers,
                      value: floors,
                      onChanged: (val) => setState(() => floors = val),
                    ),
                    const Divider(color: Color(0xFF334155)),
                    _buildCounterTile(
                      title: tr('Số phòng ngủ (Bedrooms)', 'Bedrooms'),
                      icon: Icons.bed,
                      value: bedrooms,
                      onChanged: (val) => setState(() => bedrooms = val),
                    ),
                    const Divider(color: Color(0xFF334155)),
                    _buildCounterTile(
                      title: tr('Số phòng tắm (Bathrooms)', 'Bathrooms'),
                      icon: Icons.bathtub,
                      value: bathrooms,
                      onChanged: (val) => setState(() => bathrooms = val),
                    ),
                    const SizedBox(height: 14),

                    // Direction Selectors
                    Row(
                      children: [
                        Expanded(
                          child: DropdownButtonFormField<String>(
                            value: houseDirection,
                            decoration: InputDecoration(
                              labelText: tr('Hướng nhà', 'House Direction'),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                              isDense: true,
                              filled: true,
                              fillColor: const Color(0xFF0F172A),
                            ),
                            items: houseDirections.map((d) => DropdownMenuItem(value: d, child: Text(d))).toList(),
                            onChanged: (v) => setState(() => houseDirection = v!),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: DropdownButtonFormField<String>(
                            value: balconyDirection,
                            decoration: InputDecoration(
                              labelText: tr('Hướng ban công', 'Balcony Direction'),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                              isDense: true,
                              filled: true,
                              fillColor: const Color(0xFF0F172A),
                            ),
                            items: houseDirections.map((d) => DropdownMenuItem(value: d, child: Text(d))).toList(),
                            onChanged: (v) => setState(() => balconyDirection = v!),
                          ),
                        ),
                      ],
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
                gradient: const LinearGradient(
                  colors: [Color(0xFFF59E0B), Color(0xFFD97706)],
                ),
                boxShadow: [
                  BoxShadow(
                    color: const Color(0xFFF59E0B).withOpacity(0.3),
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
                          const Icon(Icons.calculate, color: Colors.black),
                          const SizedBox(width: 8),
                          Text(
                            tr('Định Giá Ngay (AI Valuation)', 'Calculate Valuation with AI'),
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.black),
                          ),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 24),

            // Result Display
            if (predictedPrice != null) ...[
              Card(
                color: const Color(0xFF1E1B13),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                  side: const BorderSide(color: Color(0xFFF59E0B), width: 1.5),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    children: [
                      Text(
                        tr('Giá trị Ước tính Bất động sản', 'Estimated Property Valuation'),
                        style: const TextStyle(fontSize: 13, color: Color(0xFFCBD5E1)),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        '$predictedPrice $priceUnit',
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.w800,
                          color: Color(0xFFF59E0B),
                        ),
                      ),
                      const SizedBox(height: 10),

                      if (areaVal > 0 && double.tryParse(predictedPrice!) != null) ...[
                        Chip(
                          avatar: const Icon(Icons.sell, size: 14, color: Colors.amberAccent),
                          label: Text(
                            tr('Trung bình ~${((double.parse(predictedPrice!) * 1000) / areaVal).toStringAsFixed(1)} triệu / m²', 'Avg ~${((double.parse(predictedPrice!) * 1000) / areaVal).toStringAsFixed(1)} Million / m²'),
                            style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                          ),
                          backgroundColor: Colors.amber.withOpacity(0.15),
                        ),
                        const SizedBox(height: 10),
                      ],

                      if (modelUsed != null)
                        Text(
                          tr('Thuật toán AI sử dụng: $modelUsed', 'AI Model Algorithm: $modelUsed'),
                          style: const TextStyle(fontSize: 11, color: Color(0xFF94A3B8)),
                        ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 14),

              // Raw JSON
              ExpansionTile(
                title: Text(tr('Xem phản hồi JSON gốc', 'View Raw JSON Response'), style: const TextStyle(fontSize: 13, color: Color(0xFF94A3B8))),
                children: [
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: const Color(0xFF0F172A),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      rawJson,
                      style: const TextStyle(fontFamily: 'monospace', fontSize: 11, color: Color(0xFFF59E0B)),
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
