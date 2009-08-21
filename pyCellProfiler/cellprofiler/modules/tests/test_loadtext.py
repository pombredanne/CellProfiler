'''test_loadtext - Test the LoadText module

CellProfiler is distributed under the GNU General Public License.
See the accompanying file LICENSE for details.

Developed by the Broad Institute
Copyright 2003-2009

Please see the AUTHORS file for credits.

Website: http://www.cellprofiler.org
'''
__version = "$Revision$"

import base64
import numpy as np
import os
import re
from StringIO import StringIO
import tempfile
import unittest
import zlib

import cellprofiler.pipeline as cpp
import cellprofiler.cpmodule as cpm
import cellprofiler.cpimage as cpi
import cellprofiler.measurements as cpmeas
import cellprofiler.objects as cpo
import cellprofiler.workspace as cpw
import cellprofiler.modules.loadtext as L
from cellprofiler.modules.tests import example_images_directory

class TestLoadText(unittest.TestCase):
    def make_pipeline(self, csv_text):
        handle, name = tempfile.mkstemp("csv")
        fd = os.fdopen(handle, 'w')
        fd.write(csv_text)
        fd.close()
        csv_path, csv_file = os.path.split(name) 
        module = L.LoadText()
        module.csv_directory_choice.value = L.DIR_OTHER
        module.csv_custom_directory.value = csv_path
        module.csv_file_name.value = csv_file
        module.module_num = 1
        pipeline = cpp.Pipeline()
        pipeline.add_module(module)
        def error_callback(caller, event):
            self.assertFalse(isinstance(event, cpp.RunExceptionEvent))
        pipeline.add_listener(error_callback)
        return pipeline, module, name
    
    def test_01_00_revision(self):
        '''Remember to update this and write another test on new revision'''
        self.assertEqual(L.LoadText().variable_revision_number, 2)
        
    def test_01_01_load_v1(self):
        data = ('eJztV01v2jAYdvgabBPith59mnrootANqeWyMtAEU6EVRdV2qlwwzJITR46'
                'DYL9gP2nHHfdz9hNm06QkHiUQsXXSsGQlr/0+z/tlJ3a3MThvvIM104Ldxu'
                'DVmFAMLykSY8btOnTEEWxyjAQeQebU4eCzDz/4DqyewGqt/vq4btXgsWWdg'
                'nTN6HTL8nFYAaAgn0XZM8FUPpCNSFfyFRaCOBMvD3LgIBj/Lvs14gTdUnyN'
                'qI+9pYlwvOOM2WDu3k912cinuIfsqLJsPd++xdy7GIfAYPqSzDC9Il+wFkK'
                'o1sdT4hHmBPiAXx+9t8uEZlfl4aCwzIOh5SGrjSv9Nljq51bk7UVEvxLILT'
                'xGPhWwY6MJhi3C8VAwPl/wWQl82RhfFrR6jQXuLAFX0vxQcnMumEuRZ0fiS'
                'bJvxHgMYAa4kwRcEcTtK/m9rOdIBrCJ/2UNXw7xkSDS+lG13pyaQ2+6Cf6J'
                'hldyk3G+aR1WxdG86PdvtDi2XQef5FrexP+CZl/JLTIlI7xZ/pLwu94PSfl'
                '8rvEpuccgx94QUfmRAkGOd8WTdn9EcQUNF7YQVwqeu8Kt8jMT8zMjY30cP1'
                'Pt16Oqpdpj+Psjv93/Ia2ds4S8PNXyomSi9s+EM9/dPc+fiqOi2a/E7EPij'
                'LC7S57/vR573B63xy1xX42Hv+f6OUvpfwTr9+9LEN+/Sh5iSl3O1L2Om/bi'
                '8uGZlKGRwDNhnsuXgXy5458l8Lc1/vZD/EN5KJXnKEKpbxMHCXkDukGuS+d'
                'm826mE51pqJl/wX60jqUV9qP1yEipmM+vrb9e9+V6+Pk2jT3DMH47tzxLwO'
                'UiPqmm8N/AduvucI1+GOPf0v8FsdkNYQ==')
        fd = StringIO(zlib.decompress(base64.b64decode(data)))
        pipeline = cpp.Pipeline()
        pipeline.load(fd)
        self.assertEqual(len(pipeline.modules()),3)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module,L.LoadText))
        self.assertEqual(module.csv_directory_choice, L.DIR_DEFAULT_IMAGE)
        self.assertEqual(module.csv_file_name, "1049.csv")
        self.assertTrue(module.wants_images.value)
        self.assertFalse(module.wants_image_groupings.value)
        self.assertEqual(module.image_directory_choice, L.DIR_DEFAULT_IMAGE)
        self.assertFalse(module.wants_rows.value)
    
    def test_01_02_load_v2(self):
        data = ('eJztVd1KwzAUTuv82QTxTi9zJV5oycTf3eimiAM3xQ3RK4lbOgJpM9J0bD6B'
                'j+Jj+Cg+go9gMtKtrWOdeiPogZCc5PvOyfk4bWrl5mW5AvccBGvl5rZLGYHX'
                'DEuXC68EfbkFTwXBkrQh90vwXFBYDjsQHcDifqmISmgX7iB0BL5nVrW2oqa3'
                'RQAW1Lykhm2O5o1vxYb2G0RK6neCeZAD62b/VY1bLCh+ZOQWs5AE4xTRftV3'
                'eXPQHR3VeDtkpI69OFhZPfQeiQiu3Ihojq9pn7AGfSKpEiLYDenRgHLf8E38'
                '9O4oL5epvFqHF3usgzVBh0JsX+MvwBifm4Bfi+FXjX9GXBwyCase7hB4RgVp'
                'SS4Gw3goI56ViGcBx9zjMIO3BJL30H4R7R45raA3S965BH8O3CvtflP9WTw7'
                'wbNBnf9At60i0vYT3U4yePlUXu03Ko2HNg9GXavj3H2xX+P3XUjhI4vw+X/e'
                'n+c9g+n9Ff8eh/0Ipvf1Bkj2tfZbhLGu4PrdE443/DkHDuO4LUlfOpdq0VSL'
                'z3XkJ8SP38dWq0JG/em6x3q8H38nnz0h33IGL2de3LR+s+i9OQUPUvgPhsiG'
                'ig==')
        pipeline = cpp.Pipeline()
        def callback(caller,event):
            self.assertFalse(isinstance(event, cpp.LoadExceptionEvent))
        pipeline.add_listener(callback)
        pipeline.load(StringIO(zlib.decompress(base64.b64decode(data))))
        self.assertEqual(len(pipeline.modules()), 1)
        module = pipeline.modules()[0]
        self.assertTrue(isinstance(module,L.LoadText))
        self.assertEqual(module.csv_file_name, "1049.csv")
        self.assertTrue(module.wants_images.value)
        self.assertTrue(module.wants_image_groupings.value)
        self.assertEqual(len(module.metadata_fields.selections),1)
        self.assertEqual(module.metadata_fields.selections[0], "SBS_doses")
        self.assertEqual(module.image_directory_choice, L.DIR_DEFAULT_IMAGE)
        self.assertFalse(module.wants_rows.value)
        
    def test_02_01_string_image_measurement(self):
        csv_text = '''"Test_Measurement"
"Hello, world"
'''
        pipeline, module, filename = self.make_pipeline(csv_text)
        m = pipeline.run()
        data = m.get_current_image_measurement("Test_Measurement")
        self.assertEqual(data, "Hello, world")
        os.remove(filename)
    
    def test_02_02_float_image_measurement(self):
        csv_text = '''"Test_Measurement"
1.5
'''
        pipeline, module, filename = self.make_pipeline(csv_text)
        m = pipeline.run()
        data = m.get_current_image_measurement("Test_Measurement")
        self.assertAlmostEqual(data, 1.5)
        os.remove(filename)
    
    def test_02_02_int_image_measurement(self):
        csv_text = '''"Test_Measurement"
1
'''
        pipeline, module, filename = self.make_pipeline(csv_text)
        m = pipeline.run()
        data = m.get_current_image_measurement("Test_Measurement")
        self.assertEqual(data, 1)
        os.remove(filename)
    
    def test_03_01_metadata(self):
        csv_text = '''"Metadata_Plate"
"P-12345"
'''
        pipeline, module, filename = self.make_pipeline(csv_text)
        m = pipeline.run()
        data = m.get_current_image_measurement("Metadata_Plate")
        self.assertEqual(data, "P-12345")
        os.remove(filename)

    def test_04_01_load_file(self):
        dir = os.path.join(example_images_directory(), "ExampleSBSImages")
        csv_text = '''"Image_FileName_DNA","Image_PathName_DNA"
"Channel2-01-A-01.tif","%s"
'''%(dir)
        pipeline, module, filename = self.make_pipeline(csv_text)
        c0_ran = [False]
        def callback(workspace):
            imgset = workspace.image_set
            image = imgset.get_image("DNA")
            pixels = image.pixel_data
            self.assertEqual(pixels.shape[0],640)
            c0_ran[0] = True
            
        c0 = C0(callback)
        c0.module_num = 1
        pipeline.add_module(c0)
                
        try:
            m = pipeline.run()
            self.assertTrue(c0_ran[0])
            hexdigest = m.get_current_image_measurement('MD5Digest_DNA')
            self.assertEqual(hexdigest, 'c55554be83a1c928c1ae9268486a94b3')
        finally:
            os.remove(filename)
    
    def test_04_02_dont_load_file(self):
        dir = os.path.join(example_images_directory(), "ExampleSBSImages")
        csv_text = '''"Image_FileName_DNA","Image_PathName_DNA"
"Channel2-01-A-01.tif","%s"
'''%(dir)
        pipeline, module, filename = self.make_pipeline(csv_text)
        c0_ran = [False]
        def callback(workspace):
            imgset = workspace.image_set
            self.assertEqual(len(imgset.get_names()),0)
            c0_ran[0] = True
        c0 = C0(callback)
        c0.module_num = 1
        pipeline.add_module(c0)
        try:
            module.wants_images.value = False
            pipeline.run()
            self.assertTrue(c0_ran[0])
        finally:
            os.remove(filename)
    
    def test_05_01_some_rows(self):
        csv_text = '''"Test_Measurement"
1
2
3
4
5
6
7
8
9
10
'''
        pipeline, module, filename = self.make_pipeline(csv_text)
        module.wants_rows.value = True
        module.row_range.min = 4
        module.row_range.max = 6
        m = pipeline.run()
        self.assertTrue(isinstance(m, cpmeas.Measurements))
        data = m.get_all_measurements(cpmeas.IMAGE, "Test_Measurement")
        self.assertTrue(np.all(data == np.arange(4,7)))
        os.remove(filename)
    
    def test_06_01_alternate_image_start(self):
        csv_text = '''"Metadata_Measurement"
1
2
3
4
5
6
7
8
9
10
'''
        pipeline, module, filename = self.make_pipeline(csv_text)
        m = pipeline.run(image_set_start=2)
        data = m.get_all_measurements(cpmeas.IMAGE, "Metadata_Measurement")
        self.assertTrue(all([data[i-2] == str(i) for i in range(2,11)]))
        os.remove(filename)
    
    def test_07_01_get_measurement_columns(self):
        '''Test the get_measurement_columns method'''
        colnames = ('Integer_Measurement','Float_Measurement','String_Measurement')
        coltypes = [cpmeas.COLTYPE_INTEGER,cpmeas.COLTYPE_FLOAT,
                    cpmeas.COLTYPE_VARCHAR_FORMAT%9]
        csv_text = '''"%s","%s","%s"
1,1,1
2,1.5,"Hi"
3,1,"Hello"
4,1.7,"Hola"
5,1.2,"Bonjour"
6,1.5,"Gutentag"
7,1.1,"Hej"
8,2.3,"Bevakasha"
'''%colnames
        pipeline, module, filename = self.make_pipeline(csv_text)
        columns = module.get_measurement_columns(None)
        for colname, coltype in zip(colnames, coltypes):
            self.assertTrue(any([(column[0] == cpmeas.IMAGE and
                                  column[1] == colname and
                                  column[2] == coltype) for column in columns]),
                            'Failed to find %s'%colname)
        os.remove(filename)
    
    def test_08_01_get_groupings(self):
        '''Test the get_groupings method'''
        dir = os.path.join(example_images_directory(), "ExampleSBSImages")
        pattern = 'Channel1-[0-9]{2}-(?P<ROW>[A-H])-(?P<COL>[0-9]{2})\\.tif'
        csv_text ='"Image_FileName_Cytoplasm","Image_PathName_Cytoplasm","Metadata_ROW","Metadata_COL"\n'
        for filename in os.listdir(dir):
            match = re.match(pattern, filename)
            if match:
                csv_text += ('"%s","%s","%s","%s"\n' %
                             (filename, dir, match.group("ROW"), 
                              match.group("COL")))
        pipeline, module, filename = self.make_pipeline(csv_text)
        self.assertTrue(isinstance(module, L.LoadText))
        module.wants_images.value = True
        module.wants_image_groupings.value = True
        module.metadata_fields.value = "ROW"
        image_set_list = cpi.ImageSetList()
        module.prepare_run(pipeline, image_set_list, None)
        keys, groupings = module.get_groupings(image_set_list)
        self.assertEqual(len(keys), 1)
        self.assertEqual(keys[0], "ROW")
        self.assertEqual(len(groupings), 8)
        self.assertTrue(all([g[0]["ROW"] == row for g, row in zip(groupings, 'ABCDEFGH')]))
        for grouping in groupings:
            row = grouping[0]["ROW"]
            module.prepare_group(pipeline, image_set_list, grouping[0], grouping[1])
            for image_number in grouping[1]:
                image_set = image_set_list.get_image_set(image_number-1)
                self.assertEqual(image_set.keys["ROW"], row)
                provider = image_set.get_image_provider("Cytoplasm")
                match = re.search(pattern, provider.get_filename())
                self.assertTrue(match)
                self.assertEqual(row, match.group("ROW"))

class C0(cpm.CPModule):
    module_name = 'C0'
    def __init__(self, callback):
        self.callback = callback
        
    def run(self, workspace):
        self.callback(workspace)
                