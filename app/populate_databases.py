# TODO: 050920
# Update this bad boy to whatever is on the doc now
# Create a way (a route on the app) to move all of these onto the database

monster_query = """
CREATE TABLE reporting_entities(
   id              STRING(1000) NOT NULL PRIMARY KEY
  ,name            STRING(1000) NOT NULL
  ,primary_display BOOLEAN  NOT NULL
  ,status          STRING(1000) NOT NULL
  ,osm_id          STRING(1000) NOT NULL
  ,centerpoint     STRING(1000) NOT NULL
);
INSERT INTO reporting_entities(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings','kings',TRUE,'accepted','osm','cp');
INSERT INTO reporting_entities(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.k1','kings k1',FALSE,'accepted','osm1','cp1');
INSERT INTO reporting_entities(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.k2','kings k2',FALSE,'accepted','osm2','cp2');
INSERT INTO reporting_entities(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.kings.k3','kings k3',FALSE,'submitted','osm3','cp3');
INSERT INTO reporting_entities(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.corpuschristi','corpus christi',TRUE,'accepted','osm4','cp4');
INSERT INTO reporting_entities(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.corpuschristi.cc1','corpus christi cc1',FALSE,'accepted','osm5','cp5');
INSERT INTO reporting_entities(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.corpuschristi.cc2','corpus christi cc2',FALSE,'accepted','osm6','cp6');
INSERT INTO reporting_entities(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.corpuschristi.cc3','corpus christi cc3',FALSE,'rejected','osm7','cp7');
INSERT INTO reporting_entities(id,name,primary_display,status,osm_id,centerpoint) VALUES ('uk.ac.cam.christ','christ',TRUE,'submitted','osm8','cp8');

CREATE TABLE entity_properties(
   id           CHAR(1000) NOT NULL
  ,property     CHAR(1000) NOT NULL
  ,is_numeric   BOOLEAN  NOT NULL
  ,numb_value   INT 
  ,string_value CHAR(1000)
  ,PRIMARY KEY (id, property)
);
INSERT INTO entity_properties(id,property,is_numeric,numb_value,string_value) VALUES ('uk.ac.cam.kings','kings main',TRUE,4000,NULL);
INSERT INTO entity_properties(id,property,is_numeric,numb_value,string_value) VALUES ('uk.ac.cam.kings.k1','kings bodleys',TRUE,50,NULL);
INSERT INTO entity_properties(id,property,is_numeric,numb_value,string_value) VALUES ('uk.ac.cam.kings.k2','kings garden',FALSE,NULL,'next to Fellow''s garden');
INSERT INTO entity_properties(id,property,is_numeric,numb_value,string_value) VALUES ('uk.ac.cam.kings.k3','kings market',FALSE,NULL,'next to marketplace');
INSERT INTO entity_properties(id,property,is_numeric,numb_value,string_value) VALUES ('uk.ac.cam.corpuschristi','cc main num',TRUE,2000,NULL);
INSERT INTO entity_properties(id,property,is_numeric,numb_value,string_value) VALUES ('uk.ac.cam.corpuschristi','cc main',FALSE,NULL,'translates to christ\'s pieces');
INSERT INTO entity_properties(id,property,is_numeric,numb_value,string_value) VALUES ('uk.ac.cam.corpuschristi.cc2','cc building 2',TRUE,30,NULL);
INSERT INTO entity_properties(id,property,is_numeric,numb_value,string_value) VALUES ('uk.ac.cam.corpuschristi.cc3','cc building 3',TRUE,60,NULL);
INSERT INTO entity_properties(id,property,is_numeric,numb_value,string_value) VALUES ('uk.ac.cam.christ','christ main',TRUE,1500,NULL);




CREATE TABLE subentities(
  entity_id	STRING(1000) NOT NULL PRIMARY KEY REFERENCES reporting_entites(id)
  ,subentity_id	STRING(1000) NOT NULL PRIMARY KEY REFERENCES reporting_entites(id)
);
INSERT INTO subentities(entity_id,subentity_id) VALUES ('uk.ac.cam.kings','uk.ac.cam.kings.k1');
INSERT INTO subentities(entity_id,subentity_id) VALUES ('uk.ac.cam.kings','uk.ac.cam.kings.k2');
INSERT INTO subentities(entity_id,subentity_id) VALUES ('uk.ac.cam.kings','uk.ac.cam.kings.k3');
INSERT INTO subentities(entity_id,subentity_id) VALUES ('uk.ac.cam.corpuschristi','uk.ac.cam.corpuschristi.cc1');
INSERT INTO subentities(entity_id,subentity_id) VALUES ('uk.ac.cam.corpuschristi','uk.ac.cam.corpuschristi.cc2');
INSERT INTO subentities(entity_id,subentity_id) VALUES ('uk.ac.cam.corpuschristi','uk.ac.cam.corpuschristi.cc3');
INSERT INTO subentities(entity_id,subentity_id) VALUES ('uk.ac.cam.christ','uk.ac.cam.christ.c1');


CREATE TABLE user_to_entity(
   user_id   VARCHAR(1000) NOT NULL
  ,entity_id VARCHAR(1000) NOT NULL
  ,role      VARCHAR(1000) NOT NULL
);
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id','uk.ac.cam.kings','metadata');
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id','uk.ac.cam.kings.k1','emission');
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id','uk.ac.cam.kings.k2','metadata');
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('john_id','uk.ac.cam.kings.k3','metadata');
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('jane_id','uk.ac.cam.corpuschristi','metadata');
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('jane_id','uk.ac.cam.corpuschristi.cc1','emission');
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('jane_id','uk.ac.cam.corpuschristi.cc2','metadata');
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('jane_id','uk.ac.cam.corpuschristi.cc3','metadata');
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('eve_id','uk.ac.cam.christ','metadata');
INSERT INTO user_to_entity(user_id,entity_id,role) VALUES ('eve_id','uk.ac.cam.christ.c1','emission');



"""