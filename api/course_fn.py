from robots import Human
import json
import re
import xmltodict
from robots.fn import benchmark, errors, log, lang, cleanQueryString, writeFile,slugify,print_single_line,formatBytes
from robots.config import linkedin_learning_url
from bs4 import BeautifulSoup
from config.cli_config import cli_config, db_path, cookie_path,browser_cache_dir,download_dir
import validators
import sys
import time
from datetime import datetime
from robots.human import Human
import os

def downloadPipe(url,human=None):
    # print(f"Downloading:{output_filename}")
    # print(f"url:{url}")

    if not human:
        human = Human(cookie_path, browser_cache_dir)
    browser=human.getBrowser()
    requests=browser.getSession()
    block_size = int(1024*(1024/5)) #1 Kibibyte
    byte_written = 0
    resp = requests.get(url, stream=True, allow_redirects=True)
    total_size_in_bytes= int(resp.headers.get('content-length', 0))
    if resp.status_code != 200:
        # print(resp.status_code)
        sys.exit()
    # with open(output_filename, 'wb') as file:
    sys.stdout.flush()
    for data in resp.iter_content(block_size):
        byte_written += len(data)
        # print_single_line(f"downloading {byte_written} KB")
        # print(byte_written)
        sys.stdout.buffer.write(data)
# .write(data)
    if 'Transfer-Encoding' in resp.headers:
        if resp.headers['Transfer-Encoding'] == 'chunked' and byte_written > 0:
            # toc.dlVideoSize = byte_written
            # toc.dlVideoComplete = 1
            # db.session.commit()
            sys.stdout.buffer.write(data)

def downloadFile(url,output_filename,human=None):
    mo_rel_path = os.path.relpath(output_filename, f"{os.path.dirname(__file__)}/../../")

    print(f"Downloading:{mo_rel_path}")
    print(f"url:{url}")

    if not human:
        human = Human(cookie_path, browser_cache_dir)
    browser=human.getBrowser()
    requests=browser.getSession()
    block_size = int(1024*(1024/5)) #1 Kibibyte
    byte_written = 0
    resp = requests.get(url, stream=True, allow_redirects=True)
    if resp.status_code == 401:
        errors(f"server send status code 401")
    else:
        total_size_in_bytes= int(resp.headers.get('content-length', 0))

        with open(output_filename, 'wb') as file:
            for data in resp.iter_content(block_size):
                byte_written += len(data)
                print_single_line(f"downloading {formatBytes(byte_written)}")
                file.write(data)
            if 'Transfer-Encoding' in resp.headers:
                if resp.headers['Transfer-Encoding'] == 'chunked' and byte_written > 0:
                    # toc.dlVideoSize = byte_written
                    # toc.dlVideoComplete = 1
                    # db.session.commit()
                    file.write(data)
    return resp.status_code

def getDownloadDir(course_slug):
    path = download_dir
    if not os.path.exists(path):
        os.makedirs(path)
        print("MKDIR : %s " %(path))
    path = path + "/" + course_slug 
    if not os.path.exists(path):
        os.makedirs(path)
        print("MKDIR : %s " %(path))
    return path

def isTimeExpired(tm_stamp):
    exp_dt = datetime.fromtimestamp(tm_stamp)
    curr_stamp = datetime.now().timestamp()
    curr_dt = datetime.fromtimestamp(curr_stamp)

    return exp_dt <= curr_dt

def slugToTitle(slug):
    words = slug.split('-')
    title_case_words = [word.capitalize() for word in words]
    return ' '.join(title_case_words)

def getNText(**kwargs):
    args=kwargs
    nd=args["p"]
    c=args["c"]
    text=""
    if type(c) == list:
        max_len=len(c)-1
        idx=0
        c_el=nd
        break_the_loop=False
        for ic in c:
            ic_el = c_el.find(ic)
            if not ic_el or break_the_loop:
                break
            if idx >= max_len:
                if ic_el:
                    text=ic_el.text.strip()
            else:
                c_el = ic_el
            idx+=1
    else:
        c_nd = nd.find(c)
        if c_nd:
            text=c_nd.text.strip()
    return text

def getAuthors(doc,m_author,course):
    p,course_urn = getCourseXmlParentElement(doc)
    author_els=p.find_all("authors")
    authors=[]
    for author_el in author_els:
        author_urn = author_el.text.strip()
        author_entity_el=doc.find("entityUrn",text=author_urn)
        if author_entity_el:
            author_entity_el_p = author_entity_el.parent
            slug = getNText(p=author_entity_el_p,c='slug')
            name=slugToTitle(slug)
            biography=getNText(p=author_entity_el_p,c=['biographyV2','text'])
            shortBiography=getNText(p=author_entity_el_p,c=['shortBiographyV2','text'])
            author=m_author.create(slug=slug, name=name, biography=biography, shortBiography=shortBiography)
            authors.append(author)
            m_author.addCourse(author,course)
    return authors

def getCourseInfo(doc):
   
    p,course_urn = getCourseXmlParentElement(doc)
    if p:
        course_slug = p.find('slug').text
        data={
            "url" : "%s/%s" % (linkedin_learning_url, course_slug),
            "slug" : course_slug,
            "exerciseFiles" : None,
            "sourceCodeRepository": None,
            "description" : None,
            "urn" : course_urn
        }
        title = p.find('title')
        if title:
            data["title"] = title.text

        visibility = p.find('visibility')
        
        if visibility:
            data["visibility"] = visibility.text

        viewerCounts = p.find('viewerCounts')
        if viewerCounts:
            viewerCounts = viewerCounts.find('total')
            if viewerCounts:
                data["viewerCounts"] = int(viewerCounts.text)

        description = p.find('description')
        
        if description:
            description = description.find('text')
            if description:
                data["description"] = description.text

        descriptionv2 = p.find('descriptionV2')
        
        if descriptionv2:
            descriptionv2 = descriptionv2.find('text')
            if descriptionv2:
                data["descriptionV2"] = descriptionv2.text
                data["description"] = data["descriptionV2"] 

        duration = p.find('duration')
        if duration:
            duration = duration.find('duration')
            if duration:
                data["duration"] = int(duration.text)
        
        dificulty = p.find('dificulty')

        if dificulty:
            dificulty = dificulty.find('difficultylevel')
            if dificulty:
                data["dificulty"] = dificulty.text


        descriptionv3 = p.find('descriptionV3')

        if descriptionv3:
            descriptionv3 = descriptionv3.find('text')
            if descriptionv3:
                data["descriptionV3"] = descriptionv3.text
                data["description"] = data["descriptionV3"] 


        sourceCodeRepo=p.find('sourceCodeRepository')
        if sourceCodeRepo:
            data["sourceCodeRepository"]=sourceCodeRepo.text

        tags = ["sizeInBytes","name","url"]
        exerciseFiles = p.find('exerciseFiles')
        if exerciseFiles:
            for tag in tags:
                exercise_file_nd = exerciseFiles.find(tag) 
                if exercise_file_nd:
                    exercise_file_nd = exercise_file_nd.text
                    if exercise_file_nd:
                        if not data["exerciseFiles"]:
                            data["exerciseFiles"]={}
                        if tag == "sizeInBytes":     
                            data["exerciseFiles"][tag]=int(exercise_file_nd)
                        else:
                            data["exerciseFiles"][tag]=exercise_file_nd

    # data["primaryThumbnailV2"]=xmltodict.parse(str(p("primaryThumbnailV2")))
    # data["authors"]=xmltodict.parse(str(p("authors")))
    
    # authorsV2=p.find("authorsV2")
    # print(authorsV2)
    # data["authorsV2"]=xmltodict.parse(str(p("authorsv2")))
    # primarythumbnailv2
    # features > contentrating
    # urn star
    #   authors
    #   contents
    

    #  authorsv2
    # print(p("contents")) 
    # print(data)

            
    return data
    # return None



def getCourseSections(p,doc, m_section, courseId):
    sections = m_section.getListCourseId(courseId)
    if sections:
        return sections
    course_section_stars = p.find_all("contents")
    sections=[]
    tocs={}
    for section_star in course_section_stars:
        section_star = section_star.text.strip()
        section_nd = doc.find('cachingKey',text=section_star)
        # print("213:%s" % section_star)
        if section_nd:
            section_nd_p = section_nd.parent
            section_title=section_nd_p.find("title")
            if section_title:
                section_title = section_title.text.strip()
                # print(section_title)
                section_slug=slugify(section_title)
                tocs[section_slug] = []
                section = {
                    "title" : section_title,
                    "item_stars" : [],
                    "slug":section_slug
                }
                item_star_nds = section_nd_p.find_all("star_items")
                # item_stars=[]
                if item_star_nds:
                    for item_star_el in item_star_nds:
                        item_star = item_star_el.text.strip()
                        skip_pattern=r"urn:li:learningApiTocItem:urn:li:learningApiAssessmen"
                        match_skip_pattern=re.findall(skip_pattern,  item_star)
                        if len(match_skip_pattern)>0:
                            continue
                        section["item_stars"].append(item_star)
                        # item_stars.append(item_star)
                        # toc = getCourseToc(item_star,doc,course_slug,json_config)
                        # if toc:
                        #     tocs[section_slug].append(toc)
            
                s=m_section.create(courseId, section_slug, section_title, [], section["item_stars"])
                sections.append(s)


    return sections  

def courseUrl(course_slug):
    return f'https://www.linkedin.com/learning/{course_slug}'

def getCourseSlugFromUrl(url):
    if not validators.url(url):
        return None
    if not isLinkedinLearningUrl(url):
        return None
    
    url=cleanQueryString(url)
    base_url = 'https://www.linkedin.com/learning/'
    slugs = url.replace(base_url,'').split('/')
    course_slug = slugs[0]
    toc_slug = None
    if len(slugs)>1:
        toc_slug = slugs[1]

    return [course_slug, toc_slug]

def isLinkedinLearningUrl(url):
    pattern = r'^https://www\.linkedin\.com/learning/'
    return re.match(pattern, url) is not None

def parseRestLiResponse(doc):
    codes=doc.find_all("code")
    codes_dict = {}
    data={"root":{}}

    for code_nd in codes:
        code_id=code_nd.get('id')
        # capture id as key values
        key = None
        pattern = r'\d+$'
        # Use re.search to find the number at the end of the string
        match = re.search(pattern, code_id)
        if match:
            id =  match.group()
            prop = code_id.replace('-%s' % id,'')
            id = "item_%s" % id
            if not id in data["root"]:
                data["root"][id] = {}

            if prop == "datalet-bpr-guid":
                if not 'key' in data["root"][id]:
                    data["root"][id]['key'] = parseJson(code_id, code_nd)
            elif prop == "bpr-guid":
                if not 'value' in data["root"][id]:
                    data["root"][id]['value'] = parseJson(code_id, code_nd)
    return data

def parseJson(code_id,code_nd):
    code_content=""
    try:
        code_content=json.loads(code_nd.text)
    except Exception as e:
        errors('error parsing %s' % code_id,e)
    
    return code_content

def convert2Xml(data, page_name, cache_xml_to_file=False):
    xml_data = xmltodict.unparse(data, pretty=True)
    xml_data = xml_data.replace('<body','<tbody').replace('</body','</tbody')
    xml_data = xml_data.replace('<$','<').replace('</$','</')
    xml_data = xml_data.replace('<*','<star_').replace('</*','</star_')

    if cache_xml_to_file:
        xml_path = '%s/%s.xml' % (browser_cache_dir,page_name)
        writeFile(xml_path, xml_data)
        data = open(xml_path, 'rb')
        xml_data = data.read()
    
    doc=BeautifulSoup(xml_data,features="xml")
    return doc

def getTranscripts(v_meta_data_nd, doc,toc,m_transcript):
    transcripts=m_transcript.getByTocId(toc.id)
    if transcripts:
        log('transcripts_get_from_m_transcript')
        return transcripts
    pg_transcript_nds = []
    if v_meta_data_nd:
        pg_transcript_nds = v_meta_data_nd.find_all("transcripts")
    transcripts=None
    tags = ["captionFormat","isAutogenerated","captionFile"] 
    # print(pg_transcript_nds)
    for pg_transcript_el in pg_transcript_nds:
        locale = pg_transcript_el.find("locale")
        if locale:
            
            lang = locale.find("country")
            if lang:
                lang = lang.text.strip()
                lang = lang.lower()
                if not transcripts:
                    transcripts={}
                transcripts[lang] = {
                    "country" : lang
                }
                lang_country = locale.find("lang")
                if lang_country:
                    transcripts[lang]["lang"] = lang_country.text.strip()
                for tag in tags:
                    tag_nd = pg_transcript_el.find(tag)
                    if tag_nd:
                        value = tag_nd.text.strip()
                        if tag == 'isAutogenerated':
                            if value == "true":
                                value=1
                            else:
                                value=0

                        transcripts[lang][tag] = value
                transcripts[lang]=m_transcript.create(tocId=toc.id, lang=lang, country=transcripts[lang]["country"], fmt=transcripts[lang]["captionFormat"], url=transcripts[lang]["captionFile"],autoGenerated=transcripts[lang]["isAutogenerated"])
    return transcripts

def getStreamLocations(v_meta_data_nd, doc,toc,m_stream_location):
    stream_locations=m_stream_location.getByTocId(toc.id)
    if stream_locations:
        log('stream_locations_get_from_m_stream_location')
        return stream_locations

    pg_stream_nds = []
    if v_meta_data_nd:
        pg_stream_nds = v_meta_data_nd.find_all("progressiveStreams")
    stream_locations=None
    tags = ["size","bitRate","width","height"] 
    if pg_stream_nds:
        for pg_stream_el in pg_stream_nds:
            fmt = pg_stream_el.find("height")
            if fmt:
                fmt = fmt.text
                if fmt == "0":
                    fmt="audio"
                if not stream_locations:
                    stream_locations={}
                stream_locations[fmt] = {}
                stream_loc = pg_stream_el.find("streamingLocations")
                if stream_loc:
                    url = stream_loc.find("url")
                    if url:
                        url = url.text
                        stream_locations[fmt]["url"]=url
                        
                    expiresAt = stream_loc.find("expiresAt")
                    if expiresAt:
                        expiresAt = expiresAt.text
                        stream_locations[fmt]["expiresAt"]=int(expiresAt)/1000

                    for tag in tags:
                        tag_nd = stream_loc.find(tag)
                        if tag_nd:
                            stream_locations[fmt][tag] = int(tag_nd.text) 
                    
                    stream_locations[fmt]=m_stream_location.create(tocId=toc.id, fmt=fmt, url=stream_locations[fmt]["url"], expiresAt=stream_locations[fmt]["expiresAt"])

    return stream_locations
    # return None

def getVideoMeta(v_status_urn, doc, json_config):
    benchmark('getVideoMeta','start')

    # cache = json_config.get(v_status_urn)
    # if cache:
    #     log(lang('get_video_meta_from_cache',v_status_urn), verbose=True)
    #     b=benchmark('getVideoMeta','end')
    #     print(f"getVideoMeta time elapsed:{b['elapsed_time']}\n")
    #     return [cache[0],cache[1],777]
    # print(v_status_urn)

    # urn:li:lyndaVideoViewingStatus:urn:li:lyndaVideo:(urn:li:lyndaCourse:2491193,3099399)
    # urn:li:lyndaVideoViewingStatus:urn:li:lyndaVideo:(urn:li:lyndaCourse:2491193,3094437)
    v_status_lookups = doc.find_all('star_lyndaVideoViewingStatus',text=v_status_urn)
    # v_status_lookups = doc.find_all('included')
    status_429 = doc.find_all('status',text="429")
    statuses= doc.find_all('status')
    print(statuses)
    status=427
    if status_429:
        if len(status_429) > 0:
            status=429
            return [None,None,status]
    # print(len(status_429))
    # print(v_status_lookups)

    if not v_status_lookups:
        errors('A')
        errors(lang('could_not_find_v_status_lookup', v_status_urn))

        v_status_urn = v_status_urn.replace('urn:li:lyndaVideoViewingStatus:','')
        v_status_lookups= doc.find_all('trackingUrn', text=v_status_urn)
    
    if not v_status_lookups:
        errors('B')
        errors(lang('could_not_find_v_status_lookup', v_status_urn))
    # print(v_status_lookup)
    stream_locations = None
    transcripts = None
    # print(v_status_lookup)

    v_status_lookup=None
    v_meta_data_nd=None
    pos=-1
    if v_status_lookups:
        # print(v_status_lookup)

        break_the_loop=False
        for v_status_lookup in v_status_lookups:
            el_nd = v_status_lookup.parent 
            # parent_el = el_nd("parent")
            v_meta_data_nd = el_nd.find("presentation")
            pos=0
            if v_meta_data_nd:
                pos += 1
                v_meta_data_nd = v_meta_data_nd.find("videoPlay")
                if v_meta_data_nd:
                    pos += 1
                    v_meta_data_nd = v_meta_data_nd.find("videoPlayMetadata")
                    break_the_loop=True

                    if v_meta_data_nd:
                        pos += 1
                        stream_locations = getStreamLocations(v_meta_data_nd, doc)
                        transcripts = getTranscripts(v_meta_data_nd, doc)
                        status=300
                        if stream_locations and transcripts:
                            json_config.set(v_status_urn, [stream_locations,transcripts])
                            status=200
            if break_the_loop:
                break
    if not v_meta_data_nd:
        # print(v_status_lookup)
        errors("%s %s" % (lang('could_not_find_v_meta_data_nd_pos'),pos))
    b=benchmark('getVideoMeta','end')
    print(f"getVideoMeta time elapsed:{b['elapsed_time']}\n")  
    return [stream_locations,transcripts,status]

def getCourseToc(item_star,doc,m_toc,sectionId,course_slug):
    toc = m_toc.getByItemStar(item_star)
    if toc:
        return toc
    entity_nd_p = getTocXmlParentElement(item_star,doc)
    
    toc={
        "stream_locations" : None,
        "transcripts" : None
    }
    toc_slug = entity_nd_p.find("slug")
    if toc_slug:
        toc_slug = toc_slug.text
        toc["slug"] = toc_slug
        toc["url"] = "%s/%s/%s" % (linkedin_learning_url,course_slug,toc_slug)


    title = entity_nd_p.find("title")
    if title:
        title = title.text
        toc["title"] = title

    visibility = entity_nd_p.find("visibility") 
    if visibility:
        visibility = visibility.text
        toc["visibility"] = visibility

    duration = entity_nd_p.find("duration")
    if duration:
        # duration = duration.find("duration")
        # if duration:
        duration = duration.text
        toc["duration"] = duration
    v_status_urn = entity_nd_p.find("star_lyndaVideoViewingStatus")
    if v_status_urn:
        v_status_urn = v_status_urn.text.strip()
        toc["v_status_urn"] = v_status_urn

    # stream_locations, transcripts = getVideoMeta(toc["v_status_urn"], doc, json_config)
    # if stream_locations:
    #     toc["stream_locations"]=stream_locations
    # if transcripts:
    #     toc["transcripts"]=transcripts

    toc=m_toc.create(title=title, slug=toc_slug, url=toc["url"], duration=duration , captionUrl="", captionFmt="", sectionId=sectionId,item_star=item_star, v_status_urn=v_status_urn)

    return toc

def getTocXmlParentElement(item_star,doc):
    toc_nd = doc.find('cachingKey',text=item_star)
    entity_urn=None
    entity_nd_p=None
    if toc_nd:
        toc_nd_p = toc_nd.parent
        video_urn = toc_nd_p.find("content")
        if video_urn:
            video_urn = video_urn.find("video")
            if video_urn:
                video_urn = video_urn.text.strip()
                # print(video_urn)
                # break_the_loop=False
                entity_urn = doc.find('entityUrn',text=video_urn)
                if entity_urn:
                    entity_nd_p = entity_urn.parent
        
        if not entity_urn:
                errors(lang('could_not_find_video_entity_urn', item_star))
        
        if not video_urn:
            errors(lang('could_not_find_video_urn', item_star))

    else:
        errors(lang('could_not_find_toc_nd', item_star))
    return entity_nd_p

def getCourseXmlParentElement(doc):
    p=None
    course_urn=None
    rq_coure_nds=doc.find_all('request',text=lambda text: "/learning-api/courses" in text)
    rq_coure_nd = None
    for p in rq_coure_nds:
        rq_coure_nd = p

    match=None
    if rq_coure_nd:
        rq_coure_nd_p = rq_coure_nd.parent

        if rq_coure_nd_p:
            tbody =rq_coure_nd_p.find('tbody')
            # print(rq_coure_nd_p)

            if tbody:
                tbody = tbody.text
                pattern = r'\d+$'

                match = re.search(pattern, tbody)
    if not match:
        errors(lang('could_not_get_restli_request_body_content'))
        return None
    
    item_key='item_%s' % match.group()
    root_el = doc.find("%s" % item_key).find("value").find("data")
    # log(item_key)
    # print(root_el)
    data=None
    if root_el:
        course_urn=root_el.find("star_elements")
        if not course_urn:
            course_urn=root_el.find("entityUrn")

        if course_urn:
            course_urn = course_urn.text
            entity_urn = doc.find('entityUrn',text=course_urn)
            # print(entity_urn)
            
            if entity_urn:
                p = entity_urn.parent
            else:
                errors(lang('could_not_get_entity_urn'))
        else:
            errors(lang('could_not_get_course_urn'))
    else:
        error(lang('could_not_get_root_el'))
    return [p,course_urn]

def fetchCourseUrl(url,human=None,include_toc=False, no_cache=True):
    benchmark('course','start')
    course_url=cleanQueryString(url)
    course_slug, toc_slug=getCourseSlugFromUrl(url)
    print(f"course_slug:{course_slug}, toc_slug:{toc_slug}\n")
    # print(b)
  
    prx=Prx(human)
    # print(course_url)
    valid_course_url = courseUrl(course_slug)
    if include_toc:
        valid_course_url = f"{valid_course_url}/{toc_slug}"
    content=prx.get(valid_course_url, no_cache=no_cache)
    b=benchmark('course','end')
    print(f"time elapsed:{b['elapsed_time']}\n")
    # print(content)
    if content:
        page_name=prx.getPageName()
        doc=pq(content)
        data=parseRestLiResponse(doc)
        # print(data)
        xml_doc=convert2Xml(data, page_name)
        

        return xml_doc
    else:
        errors(lang('could_not_fetch_course_url', course_url))
        errors(lang('are_you_connected_to_internet'))
    

    return None

def fetchCourseTocUrl(url,human=None):
    return fetchCourseUrl(url, human,include_toc=True, no_cache=False)

