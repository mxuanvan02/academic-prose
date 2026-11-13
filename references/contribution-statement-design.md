# Contribution statements and scope claims

Companion to the introduction/abstract rules in SKILL.md. Use when writing or
revising the bullet list of contributions, the "ba đóng góp" paragraph, or any
sentence that states what the paper proves.

## Shape per contribution: one or two sentences, number plus cost

Each bullet names **what was measured or built**, gives **the number**, and gives
**the price paid**. Two sentences maximum. The reader must be able to act on it
without reading the results section.

Good — concrete, with the tradeoff visible:

> Chúng tôi định lượng được cái giá của ngưỡng tuyệt đối: nó kết tội oan 16/60
> nông dân trung thực (26,7%); quy tắc bền vững hạ xuống 3/60 (5,0%), nhưng với
> gian lận bỏ sót lệnh thì năng lực phát hiện tụt từ 9/9 xuống 4/9.

The failure shapes this author rejects, in the order he notices them:

1. **Method restated as a contribution** — "chúng tôi đề xuất phương pháp X dựa
trên Y". Says what was done, not what it buys. Replace with the measured effect.
2. **Benefit without cost** — "chúng tôi đề xuất quy tắc bền vững giảm oan". A rule
that reduces false accusations always costs detection power; a contribution that
omits the cost reads as marketing. State both numbers.
3. **Undefined comparison** — "cải thiện đáng kể", "hiệu quả hơn hẳn". No number,
no reference point. Either give the pair or cut the claim.

## Never claim impossibility for the layer the paper then fixes

Scope the impossibility claim to the **layer that was actually tested**, and say
where the hole *is* closed. "Lớp kiểm toán vật lý không bịt được lỗ hổng này…
lỗ hổng chỉ bịt được ở tầng khác, bằng bản ghi thiết bị (đóng góp thứ ba)" is
defensible; "có lỗ hổng không thể bịt" is not, and the author will catch it on the
first read because the paper's own third contribution contradicts it.

The general rule: an absolute ("không thể", "mọi lớp", "luôn", "không bộ lọc nào")
must survive an audit against every other claim in the same abstract, introduction
and conclusion. If another section solves it, the claim is a contradiction, not a
strong finding.

## State where the result does *not* reach

When the measured effect is large but does not propagate to the outcome readers
care about, one short sentence after the bullets prevents over-reading:

> Điểm đáng chú ý: mức tăng 33% ở đóng góp thứ hai không chuyển thành tín chỉ,
> vì VM0051 dùng hệ số chế độ nước bậc thang rời rạc.

This is the strongest sentence available when the downstream mechanism is
staircase, thresholded or floored: a technical hole need not be a financial one.

## Parenthetical statistics budget

One parenthetical per number, at first introduction, and never a confidence
interval repeated at every mention. `16/60 (26,7%)` in the body; the Wilson
interval belongs to the table or the supplement. Stacked parentheses
(`26,7% (16/60, khoảng Wilson 95%: [17,1%; 39,0%])`) are what the author flags as
"mở ngoặc lung tung".
