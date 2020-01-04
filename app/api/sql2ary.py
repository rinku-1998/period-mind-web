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
        time = result[10]
        time_string = ("%s年%s月%s日 %s:%s"%(time[:4], time[5:7], time[8:10], time[11:13], time[14:16]))
        result_dict['postTime'] = time_string
        sql_ary.append(result_dict)
       
    return sql_ary

def comment_sql2ary(sql_result):
    sql_ary = []
    for result in sql_result:
        result_dict = {}
        result_dict['accountName'] = result[0]
        result_dict['commentID'] = result[1]
        result_dict['postID'] = result[2]
        result_dict['accountID'] = result[3]
        result_dict['commentContent'] = result[4]
        time = result[6]
        time_string = ("%s年%s月%s日 %s:%s"%(time[:4], time[5:7], time[8:10], time[11:13], time[14:16]))
        result_dict['commentTime'] = time_string
        sql_ary.append(result_dict)
       
    return sql_ary