rotation_test_full:
	pipenv run python project_image_to_map.py input/2020-03-05\ Sdr\ Omme/DJI_0210.JPG output/2020-03-05/DJI_0210.JPG
	pipenv run python project_image_to_map.py input/2020-03-05\ Sdr\ Omme/DJI_0211.JPG output/2020-03-05/DJI_0211.JPG
	pipenv run python project_image_to_map.py input/2020-03-05\ Sdr\ Omme/DJI_0212.JPG output/2020-03-05/DJI_0212.JPG
	pipenv run python project_image_to_map.py input/2020-03-05\ Sdr\ Omme/DJI_0213.JPG output/2020-03-05/DJI_0213.JPG
	pipenv run python project_image_to_map.py input/2020-03-05\ Sdr\ Omme/DJI_0214.JPG output/2020-03-05/DJI_0214.JPG
	pipenv run python project_image_to_map.py input/2020-03-05\ Sdr\ Omme/DJI_0215.JPG output/2020-03-05/DJI_0215.JPG


rotation_test_partial:
	pipenv run python project_image_to_map.py input/2020-03-05\ Sdr\ Omme/DJI_0210.JPG output/2020-03-05/DJI_0210.JPG
	pipenv run python project_image_to_map.py input/2020-03-05\ Sdr\ Omme/DJI_0215.JPG output/2020-03-05/DJI_0215.JPG

rotation_test_two:
	pipenv run python project_image_to_map.py input/2020-09-30/DJI_0550.JPG output/2020-09-30/DJI_0550.JPG
	pipenv run python project_image_to_map.py input/2020-09-30/DJI_0553.JPG output/2020-09-30/DJI_0553.JPG
	pipenv run python project_image_to_map.py input/2020-09-30/DJI_0556.JPG output/2020-09-30/DJI_0556.JPG
	pipenv run python project_image_to_map.py input/2020-09-30/DJI_0559.JPG output/2020-09-30/DJI_0559.JPG
	pipenv run python project_image_to_map.py input/2020-09-30/DJI_0562.JPG output/2020-09-30/DJI_0562.JPG
	pipenv run python project_image_to_map.py input/2020-09-30/DJI_0565.JPG output/2020-09-30/DJI_0565.JPG
	pipenv run python project_image_to_map.py input/2020-09-30/DJI_0568.JPG output/2020-09-30/DJI_0568.JPG

initial_test:
	pipenv run python project_image_to_map.py input/DJI_0016.JPG output/DJI_0016.JPG
	pipenv run python project_image_to_map.py input/DJI_0177.JPG output/DJI_0177.JPG

center_of_rotation_test:
	pipenv run python project_image_to_map.py input/DJI_0177.JPG output/DJI_0177_000.JPG --yaw=0 --gsd=0.5
	pipenv run python project_image_to_map.py input/DJI_0177.JPG output/DJI_0177_045.JPG --yaw=45 --gsd=0.5
	pipenv run python project_image_to_map.py input/DJI_0177.JPG output/DJI_0177_090.JPG --yaw=90 --gsd=0.5
	pipenv run python project_image_to_map.py input/DJI_0177.JPG output/DJI_0177_135.JPG --yaw=135 --gsd=0.5
	pipenv run python project_image_to_map.py input/DJI_0177.JPG output/DJI_0177_180.JPG --yaw=180 --gsd=0.5
	pipenv run python project_image_to_map.py input/DJI_0177.JPG output/DJI_0177_225.JPG --yaw=225 --gsd=0.5
	pipenv run python project_image_to_map.py input/DJI_0177.JPG output/DJI_0177_270.JPG --yaw=270 --gsd=0.5
	pipenv run python project_image_to_map.py input/DJI_0177.JPG output/DJI_0177_315.JPG --yaw=315 --gsd=0.5

