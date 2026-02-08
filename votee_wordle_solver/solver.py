import requests
import random
import json

# ===================== 配置部分 =====================
BASE_URL = "https://wordle.votee.dev:8000"
MODE = "daily"
USE_REAL_API = True

# 读取单词表
try:
    with open("words.txt", "r", encoding="utf-8") as f:
        word_list = [line.strip().lower() for line in f if len(line.strip()) == 5]
    print(f"加载了 {len(word_list)} 个5字母单词")
except FileNotFoundError:
    print("错误：找不到 words.txt！请下载大词表放到项目文件夹")
    exit(1)

if not word_list:
    print("words.txt 为空！请检查文件内容")
    exit(1)

possible_words = word_list[:]  # 初始所有可能答案

all_results = []   # 仅在 daily 模式下累积
guesses_count = 0
solved = False

def filter_possible(feedback_list, possibles):
    """
    根据提供的反馈列表过滤可能单词
    feedback_list 可以是本次的5个，也可以是所有历史
    """
    correct_pos = {}          # pos -> must be this letter
    must_present = set()      # 必须出现的字母
    cannot_present = set()    # 完全不能出现的字母

    for r in feedback_list:
        let = r['guess']
        stat = r['result']
        pos = r['slot']
        if stat == "correct":
            correct_pos[pos] = let
        elif stat == "present":
            must_present.add(let)
        elif stat == "absent":
            cannot_present.add(let)

    filtered = []
    for word in possibles:
        ok = True

        # 检查正确位置
        for pos, required in correct_pos.items():
            if word[pos] != required:
                ok = False
                break
        if not ok:
            continue

        # 检查不能出现的字母
        if any(let in word for let in cannot_present):
            continue

        # 检查必须出现的字母
        word_set = set(word)
        if not must_present.issubset(word_set):
            continue

        filtered.append(word)

    return filtered

print(f"开始自动解 Wordle（模式: {MODE}）...")

while not solved and guesses_count < 6:
    if len(possible_words) == 0:
        print("每次全新随机谜题")
        break
    elif len(possible_words) == 1:
        guess = possible_words[0]
        print(f"\n只剩一个可能，直接猜: {guess.upper()}")
    else:
        # 开局固定信息量大的词
        if guesses_count == 0:
            guess = "salet" if "salet" in possible_words else random.choice(possible_words)
        elif guesses_count == 1:
            guess = "crane" if "crane" in possible_words else random.choice(possible_words)
        else:
            guess = random.choice(possible_words)

        print(f"\n第 {guesses_count + 1} 次猜测: {guess.upper()} (还剩 {len(possible_words)} 个可能)")

    if USE_REAL_API:
        url = f"{BASE_URL}/{MODE}"
        params = {"guess": guess, "size": 5}
        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code != 200:
                print(f"API 错误: {resp.status_code} - {resp.text}")
                break

            results = resp.json()

            # 打印完整返回（可注释掉）
            # print("完整服务器返回 JSON:")
            # print(json.dumps(results, indent=2))

            # 取最新5个反馈（假设每次返回当前猜测的 slot 0-4）
            if results:
                # 按 slot 排序，取最后5个
                sorted_results = sorted(results, key=lambda x: x['slot'])
                latest_feedback = sorted_results[-5:] if len(sorted_results) >= 5 else sorted_results

                print("最新猜测反馈:")
                for r in latest_feedback:
                    print(f"  位置 {r['slot']}: {r['guess']} → {r['result']}")

                # 根据模式决定用哪些反馈过滤
                if MODE == "daily":
                    all_results = results  # daily 累积所有
                    feedback_to_use = all_results
                else:  # random 只用本次
                    feedback_to_use = latest_feedback

                # 过滤
                possible_words = filter_possible(feedback_to_use, possible_words)
                print(f"过滤后还剩: {len(possible_words)} 个可能词")

                # 判断是否猜对
                if len(latest_feedback) >= 5 and all(r['result'] == "correct" for r in latest_feedback):
                    solved = True
                    print(f"\n🎉 成功！隐藏词是 {guess.upper()}，用了 {guesses_count + 1} 次")
                    if possible_words:
                        print("最终可能词:", ", ".join(possible_words[:10]))
            else:
                print("无反馈，跳过...")
                continue

        except Exception as e:
            print(f"请求失败: {e}")
            break

    guesses_count += 1

if not solved:
    print("\n6次用完，还没猜对。")
    if MODE == "random":
        print("提示：random 模式每次都是全新谜题，平均猜测次数会较高（随机性大）。")