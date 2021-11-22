from difflib import get_close_matches
import ast
import io
import math
import numpy as np
import json

class QueryNotFoundException(Exception):
    pass

def get_result(index_body, index_title, data,q):
    # with io.open("index_title.txt", "r", encoding="utf-8") as f:
    # 	   text = f.read()
    # index_title = ast.literal_eval(text)
    lb = index_body.keys()
    lt = index_title.keys()
    dic = list(lb) + list(lt)
    dic = list(dict.fromkeys(dic))
    sc = {}

    lq = q.split(" ")

    res_body = []
    res_title = []
    word = ''

    body_intersect = []
    final_result_body = []
    #
    title_intersect = []
    final_result_title = []
    if len(lq) > 1:

        for w in lq:
            pl_body = index_body.get(w)
            pl_title = index_title.get(w)
            if pl_body != None:
                for i in pl_body:
                    res_body.append(i[0])
            if pl_title != None:
                for j in pl_title:
                    res_title.append(j[0])
            if pl_body == None and pl_title == None:
                return 0,get_close_matches(w, dic, 5, 0.6)
        body_intersect = list(set([x for x in res_body if res_body.count(x) > 1]))
        title_intersect = list(set([x for x in res_body if res_body.count(x) > 1]))
        score_body = {}
        score_title = {}
        for i in body_intersect:
            sum_body = 0
            for w in lq:
                pl_body = index_body.get(w)
                if pl_body != None:
                    for j in pl_body:
                        if j[0] == i:
                            tf = j[1]
                            sum_body += tf * np.log10(10782 / len(pl_body))
            score_body.update({i: sum_body})
        for i in title_intersect:
            sum_title = 0
            for w in lq:
                pl_title = index_title.get(w)
                # print(pl_title)
                if pl_title != None:
                    for j in pl_title:
                        if j[0] == i:
                            tf = j[1]
                            sum_title += tf * np.log10(10782 / len(pl_title))
            score_title.update({i: sum_title})
        final_list = body_intersect + title_intersect
        final_score = {}
        final_sum = 0
        for i in final_list:
            if i in body_intersect and i in title_intersect:
                final_sum = score_body.get(i) + 47 * score_title.get(i)
            if i in body_intersect and i not in title_intersect:
                final_sum = score_body.get(i)
            if i not in body_intersect and i in title_intersect:
                final_sum = 47 * score_title.get(i)
            final_score.update({i: final_sum})
        # sort = sorted(final_score.values())
        # sort = list(dict.fromkeys(sort))
        # print(sort)

        # print('*****************************')
        # if sort.reverse() != None:
        sigle = {k: v for k, v in sorted(final_score.items(), key=lambda item: item[1])}
        sort = list(sigle.keys())
        f_result = []
        # sort = list(dict.fromkeys(sort))
        counter = 0
        for i in reversed(sort):
            result = data.get(str(i))
            result[0] = '{}...'.format(result[0][1:200])
            f_result.append(result)
            counter += 1
            if counter == 20 or counter == len(sort):
                break
            # print(i)
            # print(data.get(str(i)))
        return 1, f_result

    else:
        w = lq[0]
        sum_body = 0
        sum_title = 0
        pl_body = index_body.get(w)
        pl_title = index_title.get(w)
        if pl_body != None:
            for i in pl_body:
                res_body.append(i[0])
        if pl_title != None:
            for j in pl_title:
                res_title.append(j[0])
        if pl_body == None and pl_title == None:
            return 0,get_close_matches(w, dic, 5, 0.6)
        score_body = {}
        score_title = {}
        for i in res_body:
            sum_body = 0
            pl_body = index_body.get(w)
            if pl_body != None:
                for j in pl_body:
                    if j[0] == i:
                        tf = j[1]
                        sum_body = tf * np.log10(10782 / len(pl_body))
            score_body.update({i: sum_body})
        for i in res_title:
            sum_title = 0
            pl_title = index_title.get(w)
            if pl_title != None:
                for j in pl_title:
                    if j[0] == i:
                        tf = j[1]
                        sum_title = tf * np.log10(10782 / len(pl_title))
            score_title.update({i: sum_title})

        final_list = res_body + res_title
        final_score = {}
        final_sum = 0
        for i in final_list:
            if i in res_body and i in res_title:
                final_sum = score_body.get(i) + 47 * score_title.get(i)
            if i in res_body and i not in res_title:
                final_sum = score_body.get(i)
            if i not in res_body and i in res_title:
                final_sum = 47 * score_title.get(i)
            final_score.update({i: final_sum})
            # print(final_score)
        sigle = {k: v for k, v in sorted(final_score.items(), key=lambda item: item[1])}
        si = list(sigle.keys())
        f_result = []
        # si = list(dict.fromkeys(si))
        counter = 0
        for i in reversed(si):
            result = data.get(str(i))
            result[0] = '{}...'.format(result[0][1:200])
            f_result.append(result)
            counter += 1
            if counter == 20 or counter == len(si):
                break
        return 1,f_result
        # for i in reversed(si):
        #     print(data.get(str(i)))
        #     print(i)
