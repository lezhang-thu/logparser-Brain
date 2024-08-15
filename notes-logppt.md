# Template-free Prompt Tuning for Few-shot NER的paper总结

## 一些基本概念

### NER

Named Entity Recognition. 不是entity，则为O class；若是entity，则为named entity

具体来说，会有：coarse-grained and fine-grained entity types，如coarse为Event，fine-grained为Natural Disaster、Sports Event等

NER中的IO format意味着*just* tag the corresponding Entity Type or "O" in case the word is not a Named Entity

联系这篇paper，留意到了如下的说法：（说的应该是`switch_to_BIO`函数）"并且注意到作者代码中有IO标注替代BIO标注的函数，我也觉得IO标注可能更适合论文中EntityLM"([url](https://github.com/rtmaww/EntLM/issues/4#issuecomment-1116424449))

```
                    if label[word_idx] !='O':
                        target_token.append(label_token_to_id[label[word_idx]])
                    else:
                        target_token.append(input_idx)
```
如上的做法，显示出：entity，则替换了（`label[word_idx]`）；NOT entity，则保留（直接`input_idx`）

## code部分

paper的重点在于label，之前的ft用的是数据中的label，现在需要更换为virtual label。

留意到`train_transformer.py`中的函数`tokenize_and_align_labels`，分析如下：

其中的重点也是之前提到的`label_token_to_id`

参考别处有：
```
    label_token_to_id = {label: tokenizer.convert_tokens_to_ids(label_token) for label, label_token in label_token_map.items()}
    label_token_id_to_label = {idx:label for label,idx in label_token_to_id.items()}
```
所以问题的核心在于`label_token_map`（`label_token_id_to_label`仅仅为reverse，所以不困难）

而这个为：`label_token_map = {item:item for item in ori_label_token_map}`，其中的key-value pair中的value在之后将会被`tokenizer`映射，解释了其中奇怪的`item:item`的`dict`表达

找到源头了，为：
```
        ori_label_token_map = json.load(open(args.label_map_path, 'r'))
```
其中的`label_map_path`在`run_conll.sh`中为：`dataset/conll/label_map_timesup_ratio0.6_multitoken_top6.json`

其中内容，仅举一个例子：`"I-PER": ["Michael", "John", "David", "Thomas", "Martin", "Paul"]`

### 新的目标：`add_label_token_roberta`

`indexes[0]`和`indexes[1:]`分开计算的，但实际的意义就是：`indexes`所对应的words的embeddings的平均值来作为`I-PER`的embedding（初始的吗，后续不会修改吗）

**一些思考**：这里的做法还是很巧妙的，因为模型看到的不是实际的token，而是embedding

（还是有一个问题，模型最终的output为softmax的分布，指向的还是各个token的概率，而新加入的如`I-PER`这样的token之前pretrain时，是没有的，目前仅仅是说在输入阶段，模型是"认识"这个token）

在MLM中，`I-PER`有作为输入吗；如果没有的话，那么，输入这一端它也不成立，:(

## Final results

For those who are interested, it is called **weight tying** or **joint input-output embedding**.

见[https://stackoverflow.com/a/67065742](https://stackoverflow.com/a/67065742)

注意，对于EntLM，其有：`config.tie_word_embeddings`为`True`

Take me at least **two** days to find this subtlety.

## 对`train_transformer.py`有帮助的代码做一些总结

The first is `tokenizer.add_tokens`.

Next, `model.resize_token_embeddings` is also important!!! (weight tying happens, i.e. is kept, within)

Also, the initialization of these embeddings is also worth noting, i.e., taking the average of the words within the label words set.

Other code implementation is not perfect, so no more for learning.

## Miscellaneous

BERT is of type `BertForMaskedLM`? (the original Google BERT)

So the `forward` function of it includes `input_ids`, `labels`.

The returning result is of type `MaskedLMOutput` (typically), and the first value is `loss`.

The computing for `loss` is of `CrossEntropyLoss`, where we note the `ignore_index=-100`, which explains why `-100` repeatedly appears in the code of `train_transformer.py`.
