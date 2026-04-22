# mbti_assets.py

import json
import os
import streamlit as st
from utils.firebase_client import (
    fb_get_mbti_image_mapping, fb_get_major_image_mapping, 
    fb_get_mbti_questions, fb_get_mbti_comprehensive
)

# Hàm bổ trợ lấy đường dẫn tuyệt đối để tránh lỗi MediaFileHandler của Streamlit
def get_abs_path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))

def _load_mbti_image_mapping():
    """Đọc file cấu hình ảnh MBTI do Admin quản lý từ Firebase. Nếu không có thì dùng mặc định."""
    default_map = {
        "INTJ": "mbti_intj.png", "INTP": "mbti_intp.png", "ENTJ": "mbti_entj.png", "ENTP": "mbti_entp.png",
        "INFJ": "mbti_infj.png", "INFP": "mbti_infp.png", "ENFJ": "mbti_enfj.png", "ENFP": "mbti_enfp.png",
        "ISTJ": "mbti_istj.png", "ISFJ": "mbti_isfj.png", "ESTJ": "mbti_estj.png", "ESFJ": "mbti_esfj.png",
        "ISTP": "mbti_istp.png", "ISFP": "mbti_isfp.png", "ESTP": "mbti_estp.png", "ESFP": "mbti_esfp.png",
    }
    fb_map = fb_get_mbti_image_mapping()
    if fb_map:
        default_map.update(fb_map)
    return default_map

def get_mbti_image(mbti_type):
    """Trả về đường dẫn tuyệt đối của ảnh đại diện cho một nhóm MBTI cụ thể."""
    mapping = _load_mbti_image_mapping()
    img_name = mapping.get(mbti_type, "mbti_analyst.png")
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "images", img_name))

# Mapping ảnh cho 12 nhóm ngành — Admin có thể thay đổi qua Firebase
MAJOR_IMAGE_DEFAULT = {
    "CNTT & Kỹ thuật Máy tính": "major_cntt.png",
    "Kinh tế & Quản lý": "major_kinhtequanly.png",
    "Y tế & Sức khỏe": "major_medical.png",
    "Sư phạm & Giáo dục": "major_education.png",
    "Luật & Chính trị": "major_education.png",
    "Ngoại ngữ & Ngôn ngữ": "major_education.png",
    "Nghệ thuật & Thiết kế": "major_education.png",
    "Kỹ thuật & Công nghệ": "major_engineering.png",
    "Khoa học Tự nhiên": "major_engineering.png",
    "Khoa học Xã hội & Nhân văn": "major_education.png",
    "Nông Lâm Ngư nghiệp": "major_engineering.png",
    "Báo chí & Truyền thông": "major_business.png",
}

@st.cache_data(ttl=5)
def get_major_image(major_name):
    """Trả về đường dẫn tuyệt đối ảnh đại diện cho nhóm ngành."""
    current_map = MAJOR_IMAGE_DEFAULT.copy()
    fb_map = fb_get_major_image_mapping()
    if fb_map:
        current_map.update(fb_map)
    img_name = current_map.get(major_name, "major_it.png")
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "images", img_name))

# 1. Load cấu trúc câu hỏi động từ file quản lý (Firebase)
@st.cache_data(ttl=5)
def get_mbti_questions():
    try:
        qs = fb_get_mbti_questions()
        if qs: return qs
        
        # Fallback to local json if firebase is empty or fails
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions', 'mbti_questions.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi khi load danh sách câu hỏi: {e}")
        return []


# 2. Định nghĩa MBTI Detail (Nhóm, tiêu đề phụ, mô tả, ảnh)
@st.cache_data(ttl=5)
def get_mbti_details():
    return {
    # ---------------- 4 NHÀ PHÂN TÍCH (ANALYSTS) ----------------
    "INTJ": {
        "title": "Kiến trúc sư",
        "description": "Là những người cực kỳ độc lập, có tư duy chiến lược sâu sắc và khát khao hiểu biết không ngừng. Bạn luôn có một kế hoạch cho mọi thứ và khả năng phân tích nhạy bén để thực thi chúng.",
        "strengths": ["Tư duy chiến lược, phân tích logic nhạy bén.", "Khả năng làm việc độc lập và tập trung cao độ.", "Sáng tạo, luôn tìm tòi giải pháp đột phá.", "Kiên định và quyết đoán với mục tiêu."],
        "weaknesses": ["Đôi khi quá bảo thủ, khó chấp nhận ý kiến trái chiều.", "Khó khăn trong việc bộc lộ và thấu hiểu cảm xúc.", "Cầu toàn quá mức, dễ gây áp lực cho bản thân và đồng nghiệp.", "Thiếu kiên nhẫn với những quy trình cứng nhắc."],
        "careers": ["Quản trị chiến lược", "Phân tích dữ liệu / IT", "Kiến trúc sư hệ thống", "Nghiên cứu khoa học", "Phát triển sản phẩm"],
        "image": get_mbti_image("INTJ")
    },
    "INTP": {
        "title": "Nhà logic học",
        "description": "Sáng tạo, đam mê phân tích và logic. INTP thích đi sâu tìm hiểu nguyên lý vận hành của vũ trụ, hệ thống hơn là tham gia vào các hoạt động xã hội thường ngày.",
        "strengths": ["Khả năng suy luận logic xuất sắc.", "Giàu trí tưởng tượng, suy nghĩ nguyên bản (outside the box).", "Khách quan, đam mê tìm ra chân lý.", "Linh hoạt và cởi mở với những khám phá mới."],
        "weaknesses": ["Thường lơ đãng, ít chú ý đến thực tế xung quanh.", "Khó diễn đạt ý tưởng phức tạp cho người khác hiểu.", "Hay nghi ngờ bản thân (second-guessing).", "Không thích các quy định cứng nhắc."],
        "careers": ["Kỹ sư phần mềm", "Nhà tính toán / Toán học", "Thiết kế hệ thống máy tính", "Nhà triết học", "Nghiên cứu thị trường"],
        "image": get_mbti_image("INTP")
    },
    "ENTJ": {
        "title": "Nhà điều hành",
        "description": "Các nhà lãnh đạo bẩm sinh táo bạo, đầy trí tưởng tượng và có ý chí mạnh mẽ. ENTJ luôn tìm ra - hoặc tạo ra - một con đường để đưa bản thân và tập thể đến thành công.",
        "strengths": ["Tố chất lãnh đạo và tổ chức hiệu suất cao.", "Tự tin, quyết đoán và ý chí kiên cường.", "Tư duy tư tưởng lớn, chiến lược lâu dài.", "Giỏi truyền cảm hứng và thúc đẩy người khác."],
        "weaknesses": ["Có thể trở nên độc đoán, thiếu thấu cảm.", "Kém kiên nhẫn với sự chậm trễ hoặc kém hiệu quả.", "Thường gạt bỏ cảm xúc cá nhân.", "Đôi khi tỏ ra kiêu ngạo."],
        "careers": ["Giám đốc điều hành (CEO)", "Quản lý dự án", "Chuyên gia tài chính", "Cố vấn doanh nghiệp", "Luật sư doanh nghiệp"],
        "image": get_mbti_image("ENTJ")
    },
    "ENTP": {
        "title": "Người tranh luận",
        "description": "Thông minh, tò mò, luôn không ngừng thử thách các ý tưởng mới. ENTP có tư duy nhạy bén, thích phản biện để mổ xẻ vấn đề và tìm ra góc nhìn mới mẻ.",
        "strengths": ["Cực kỳ am hiểu, học hỏi nhanh chóng.", "Linh hoạt, nảy số cực kỳ nhanh.", "Sáng tạo, giỏi tạo ra ý tưởng đột phá.", "Lôi cuốn và có khả năng giao tiếp ấn tượng."],
        "weaknesses": ["Thích tranh luận đôi khi gây căng thẳng.", "Khó duy trì sự tập trung đến cuối cùng.", "Mau chán nếu công việc lặp đi lặp lại.", "Đôi khi bỏ qua các chi tiết thực tế nhỏ."],
        "careers": ["Doanh nhân", "Chuyên gia PR/Marketing", "Cố vấn chiến lược", "Kỹ sư hệ thống", "Nhà báo phân tích"],
        "image": get_mbti_image("ENTP")
    },

    # ---------------- 4 NHÀ NGOẠI GIAO (DIPLOMATS) ----------------
    "INFJ": {
        "title": "Người cố vấn",
        "description": "Tĩnh lặng và mang nhiều cảm hứng, có lý tưởng sâu sắc. INFJ không mệt mỏi mong muốn đem lại ảnh hưởng tích cực và hiểu thấu tâm can người khác.",
        "strengths": ["Thấu hiểu sâu sắc tâm lý con người.", "Khả năng giao tiếp tinh tế, truyền cảm hứng.", "Sáng tạo, có định hướng rõ ràng.", "Đam mê giúp đỡ và tạo ra giá trị bền vững."],
        "weaknesses": ["Rất dễ bị tổn thương, nhạy cảm với chỉ trích.", "Dễ kiệt sức vì mang vác quá nhiều cảm xúc.", "Quá cầu toàn ở lý tưởng bản thân.", "Hay khép kín, ít chia sẻ nỗi niềm riêng."],
        "careers": ["Nhà tâm lý học", "Giáo dục / Đào tạo", "Tư vấn nhân sự", "Nhà văn sáng tạo", "Thiết kế UI/UX"],
        "image": get_mbti_image("INFJ")
    },
    "INFP": {
        "title": "Người hòa giải",
        "description": "Giàu chất thơ, tốt bụng và tràn đầy vị tha. Sẵn lòng hỗ trợ các mục tiêu tốt đẹp với nội tâm hướng thiện nguyên bản, INFP luôn đi tìm ý nghĩa cuộc đời.",
        "strengths": ["Đồng cảm sâu sắc, luôn quan tâm người khác.", "Sáng tạo, trí tưởng tượng cực kỳ phong phú.", "Đam mê và tận tụy với giá trị cốt lõi.", "Cách nhìn nhận cuộc sống đa chiều, cởi mở."],
        "weaknesses": ["Quá lý tưởng hóa mọi thứ.", "Thường né tránh xung đột.", "Dễ bị lơ lửng, khó bám sát kế hoạch chi tiết.", "Đôi khi quá vị tha dẫn đến quên mất bản thân."],
        "careers": ["Sáng tạo nội dung / Nhà văn", "Biên tập viên", "Tư vấn viên", "Công tác xã hội", "Giáo viên nghệ thuật"],
        "image": get_mbti_image("INFP")
    },
    "ENFJ": {
        "title": "Người chỉ nam",
        "description": "Thủ lĩnh lôi cuốn, đầy lòng cảm thông. Luôn có khả năng lôi cuốn và truyền cảm hứng cho người khác đạt được mục tiêu chung bằng sự tử tế.",
        "strengths": ["Lãnh đạo bằng sự đồng cảm và bao dung.", "Giao tiếp xuất chúng, dễ thu phục nhân tâm.", "Đáng tin cậy, tôn trọng đồng nghiệp.", "Nhạy bén với cơ hội phát triển cộng đồng."],
        "weaknesses": ["Đôi khi lo lắng quá mức cho người khác.", "Sợ làm phật lòng mọi người.", "Trở nên giáo điều nếu quá áp đặt quan điểm tốt.", "Dễ căng thẳng khi phải đưa ra quyết định lý trí lạnh lùng."],
        "careers": ["Quản lý nhân sự (HR)", "Giám đốc truyền thông", "Chuyên gia đào tạo", "Điều phối sự kiện", "Giáo sư / Giảng viên"],
        "image": get_mbti_image("ENFJ")
    },
    "ENFP": {
        "title": "Người vận động",
        "description": "Nhiệt tình, sáng tạo và rất hòa đồng. Một tinh thần tự do không ngừng tìm kiếm ý nghĩa và những kết nối sâu sắc giữa các sự vật, hiện tượng.",
        "strengths": ["Tin tưởng người khác, thân thiện và năng động.", "Trí tưởng tượng phong phú, đầy sáng kiến.", "Khả năng nhận biết cơ hội xuất sắc.", "Giao tiếp lôi cuốn, tạo tiếng cười cho mọi người."],
        "weaknesses": ["Gặp khó khăn với các quy tắc, thủ tục hành chính.", "Đôi khi ôm đồm quá nhiều việc cùng lúc.", "Thiếu kỹ năng bám trụ dài hạn.", "Cảm xúc thất thường, hay suy nghĩ quá (overthinking)."],
        "careers": ["Tiếp thị / Quảng cáo", "Ngoại giao / Quan hệ công chúng", "Diễn viên / Giải trí", "Thiết kế đồ họa", "Tư vấn du lịch"],
        "image": get_mbti_image("ENFP")
    },

    # ---------------- 4 NGƯỜI CANH GÁC (SENTINELS) ----------------
    "ISTJ": {
        "title": "Nhà hậu cần",
        "description": "Thực tế, tận tâm và đáng tin cậy. Đề cao thực tiễn và tính kỷ luật để đảm bảo công việc được vận hành trơn tru và logic nhất.",
        "strengths": ["Đáng tin cậy và có trách nhiệm cao.", "Làm việc hệ thống, trật tự và quy củ.", "Kiên nhẫn, mạnh mẽ trước áp lực thực tế.", "Phân tích số liệu và sự thật rất chuẩn xác."],
        "weaknesses": ["Khó thích nghi với sự thay đổi đột ngột.", "Đôi khi quá bảo thủ, cứng nhắc.", "Không thoải mái khi đối mặt với cảm xúc.", "Dễ tự trách bản thân nếu công việc hỏng."],
        "careers": ["Kế toán / Kiểm toán", "Quản trị cơ sở dữ liệu", "Logistics / Cung ứng", "Kỹ sư dân dụng", "Kiểm định chất lượng"],
        "image": get_mbti_image("ISTJ")
    },
    "ISFJ": {
        "title": "Người bảo vệ",
        "description": "Đầy lòng trắc ẩn, cực kỳ tận tụy trong việc che chở, chăm sóc và bảo vệ những người xung quanh. Họ là trụ cột yên bình của xã hội.",
        "strengths": ["Tận tụy, trung thành và bảo vệ sâu sắc.", "Có khả năng nhớ chi tiết sự kiện rất tốt.", "Thực tế và có thể tin cậy tuyệt đối.", "Hay hỗ trợ bạn bè, đề cao sự hòa hợp."],
        "weaknesses": ["Quá khiêm tốn, hay đánh giá thấp bản thân.", "Kiệt sức vì làm hài lòng tất cả mọi người.", "Miễn cưỡng thay đổi.", "Dễ ôm thù nén vào trong lòng thay vì xả ra."],
        "careers": ["Chăm sóc sức khỏe / Điều dưỡng", "Quản lý hành chính", "Giáo dục mầm non / tiểu học", "Dịch vụ khách hàng", "Nhân sự"],
        "image": get_mbti_image("ISFJ")
    },
    "ESTJ": {
        "title": "Người quản lý",
        "description": "Rất xuất sắc trong việc quản lý và định hướng mọi người. Đề cao tính truyền thống, sự trật tự, tính kỷ luật và tính thực thi cao.",
        "strengths": ["Khả năng tổ chức và điều hành tuyệt vời.", "Trung thực, minh bạch, nói là làm.", "Tận tâm, theo đuổi mục tiêu quyết liệt.", "Rất giỏi duy trì an ninh, luật lệ."],
        "weaknesses": ["Cứng nhắc, khó thỏa hiệp ý tưởng phi truyền thống.", "Phán xét quá nhanh.", "Khó diễn tả cảm xúc dịu dàng.", "Chú trọng quá vào địa vị và tính hình thức."],
        "careers": ["Quản lý cấp cao", "Cảnh sát / Quân đội", "Kinh doanh / Quản trị viên", "Thẩm phán / Luật sư", "Quản trị chuỗi cung ứng"],
        "image": get_mbti_image("ESTJ")
    },
    "ESFJ": {
        "title": "Người quan tâm",
        "description": "Cực kỳ chu đáo, hòa đồng. Luôn khao khát được giúp đỡ và làm cho những người xung quanh cảm thấy được yêu thương và an toàn.",
        "strengths": ["Kết nối xã hội cực kỳ mạnh mẽ.", "Trách nhiệm cao với bạn bè gia đình.", "Sống thực tế và sẵn lòng lăn xả giúp đỡ.", "Kỹ năng làm việc nhóm hoàn hảo."],
        "weaknesses": ["Phụ thuộc nhiều vào sự công nhận của người khác.", "Ngại mâu thuẫn, dễ bị tổn thương nếu bị chê.", "Quá nhạy cảm hoặc để ý đến địa vị.", "Thiếu linh hoạt nếu vượt khỏi vùng an toàn hiểu biết."],
        "careers": ["Tổ chức sự kiện", "Giao dịch viên", "Nhân viên y tế", "Tư vấn viên", "Phát ngôn viên / Lễ tân"],
        "image": get_mbti_image("ESFJ")
    },

    # ---------------- 4 NHÀ THÁM HIỂM (EXPLORERS) ----------------
    "ISTP": {
        "title": "Người thợ thủ công",
        "description": "Sáng tạo, thực tế với khả năng sử dụng các công cụ một cách thành thạo. Giải quyết vấn đề rất thực tiễn, nhanh bén và không e ngại gian khó.",
        "strengths": ["Lạc quan và tràn đầy năng lượng thực thi.", "Sáng tạo, bộc phát trong tình huống khó.", "Giỏi xử lý tình huống khẩn cấp, giữ bình tĩnh.", "Tính linh hoạt và quan sát vấn đề cực cao."],
        "weaknesses": ["Rất dễ cảm thấy chán nản với sự nhàm chán.", "Khó tập trung lâu dài vào việc lên kế hoạch.", "Không thích các cam kết tình cảm dài hạn.", "Đôi khi hành động liều lĩnh, thiếu cân nhắc rủi ro bồi đắp. Không để ý cảm nhận của người khác."],
        "careers": ["Kỹ sư cơ khí", "Điều tra viên / Giám định", "Lập trình viên / Lắp ráp phần cứng", "Quản lý rủi ro", "Phát triển công nghệ cao"],
        "image": get_mbti_image("ISTP")
    },
    "ISFP": {
        "title": "Người nghệ sĩ",
        "description": "Linh hoạt, quyến rũ, luôn khám phá điều mới và phá vỡ các giới hạn. Sống hết mình trong từng khoảnh khắc và theo đuổi cái đẹp.",
        "strengths": ["Đam mê và giàu cảm hứng nghệ thuật.", "Rất linh hoạt, cởi mở đón nhận điều mới.", "Nhạy cảm cao với thẩm mỹ và không gian.", "Tôn trọng cuộc sống và giá trị của từng cá nhân."],
        "weaknesses": ["Dễ bị bối rối và làm việc tùy hứng.", "Không có định hướng tương lai rõ nét.", "Hay chịu tổn thương và khép mình khi áp lực.", "Né tránh đối diện trực tiếp với mâu thuẫn khốc liệt."],
        "careers": ["Thiết kế thời trang", "Nhiếp ảnh gia", "Kiến trúc sư nội thất", "Trang điểm / Làm đẹp", "Nghệ sĩ độc lập"],
        "image": get_mbti_image("ISFP")
    },
    "ESTP": {
        "title": "Người sáng lập",
        "description": "Thông minh, năng lượng dồi dào, đánh giá nhanh chóng và tận hưởng cảm giác sống trên những lằn ranh mạo hiểm. ESTP nắm bắt cơ hội tại thực tại.",
        "strengths": ["Táo bạo, dũng cảm đối mặt rủi ro.", "Giao tiếp mang tính hành động, thực tiễn cao.", "Lanh lợi, giỏi thuyết phục và thương lượng.", "Bắt nhịp cuộc sống xã hội theo bản năng tự nhiên."],
        "weaknesses": ["Khó làm việc theo lý thuyết trừu tượng dài dòng.", "Không để ý cảm giác lo lắng của người khác.", "Dễ lơ là các nguyên tắc luật pháp dài hạn.", "Cả thèm chóng chán trong học thuật."],
        "careers": ["Môi giới bất động sản", "Doanh nhân startup", "Quan hệ công chúng", "Lĩnh vực thể thao", "Chuyên viên đàm phán"],
        "image": get_mbti_image("ESTP")
    },
    "ESFP": {
        "title": "Người trình diễn",
        "description": "Năng động, nhiệt huyết. Đặt trải nghiệm làm trung tâm và lan tỏa niềm vui đến mọi người, ESFP thường là trung tâm của mọi buổi tiệc.",
        "strengths": ["Siêu quảng giao, kết bạn dễ dàng.", "Tinh ý, nhạy bén và khéo chiều người khác.", "Thực hành ngay lập tức, thẩm mỹ rất thời thượng.", "Lạc quan bẩm sinh, khả năng phục hồi tinh thần nhanh."],
        "weaknesses": ["Hay bỏ qua những cảnh báo nguy hiểm trong tương lai.", "Thiếu tổ chức, hay bỏ sót kế hoạch.", "Kém trong việc đối mặt khủng hoảng sâu sắc.", "Tập trung nhiều vào tận hưởng hơn là nhiệm vụ dài hạn."],
        "careers": ["Dịch vụ lưu trú / Nhà hàng", "Cố vấn thời trang", "Tổ chức sự kiện", "Tiếp viên hàng không", "Huấn luyện viên cá nhân"],
        "image": get_mbti_image("ESFP")
    }
}

# 2. Định nghĩa hình ảnh đại diện cho các nhóm ngành
def get_major_image_path(major_name):
    major_lower = major_name.lower()
    # Giáo dục, nhóm xã hội
    if any(k in major_lower for k in ['nhạc', 'mỹ thuật', 'văn hóa', 'quốc tế', 'ngôn ngữ', 'truyền thông', 'sư phạm', 'khoa học xã hội', 'luật']):
        return get_abs_path("assets/images/major_education.png")
    # Công nghệ / Toán
    elif any(k in major_lower for k in ['công nghệ thông tin', 'máy tính', 'toán học']):
        return get_abs_path("assets/images/major_it.png")
    # Y dược Sinh học
    elif any(k in major_lower for k in ['y dược', 'sức khỏe', 'sinh học']):
        return get_abs_path("assets/images/major_medical.png")
    # Kinh tế Quản trị
    elif any(k in major_lower for k in ['kinh tế', 'quản trị', 'tài chính', 'du lịch']):
        return get_abs_path("assets/images/major_business.png")
    # Kỹ Thuật (Nông lâm, công trình, hóa học, cơ khí)
    else:
        return get_abs_path("assets/images/major_engineering.png")

@st.cache_data(ttl=5)
def get_mbti_comprehensive():
    try:
        data = fb_get_mbti_comprehensive()
        if data:
            return data
        
        # Fallback to local json
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'mbti_comprehensive.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Lỗi khi load danh sách mbti comprehensive: {e}")
        return {}

