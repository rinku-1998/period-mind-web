def sql2ary(sql_result):
    sql_ary = []
    for result in sql_result:
        result_dict = {}
        result_dict['accountName'] = result[0]
        result_dict['postID'] = result[1]
        result_dict['accountID'] = result[2]
        result_dict['categoryID'] = result[3]
        result_dict['postContent'] = result[4]
        result_dict['postImage'] = result[5]
        result_dict['postLikeNumber'] = result[6]
        result_dict['postLikeAccount'] = result[7]
        result_dict['postCheck'] = result[8]
        result_dict['postLocation'] = result[9]
        result_dict['postTime'] = result[10]
        sql_ary.append(result_dict)
       
    return sql_ary