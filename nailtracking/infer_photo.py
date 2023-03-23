# -*- coding: utf-8 -*-

# import the necessary packages
# from object_detection.utils import label_map_util
# import tensorflow as tf
import numpy as np
import find_finger as ff
import tensorflow.compat.v1 as tf

tf.disable_v2_behavior()

args = {
    "model": "garnify_nails/nailtracking/model/export_model_008/frozen_inference_graph.pb",
    # "model":"/media/todd/38714CA0C89E958E/147/yl_tmp/readingbook/model/export_model_015/frozen_inference_graph.pb",
    "labels": "garnify_nails/nailtracking/record/classes.pbtxt",
    # "labels":"record/classes.pbtxt" ,
    "num_classes": 1,
    "min_confidence": 0.6,
    "class_model": "garnify_nails/nailtracking/model/class_model/p_class_model_1552620432_.h5"}

COLORS = np.random.uniform(0, 255, size=(args["num_classes"], 3))


def transparentize_nails(image):
    model = tf.Graph()

    with model.as_default():
        print("> ====== loading NAIL frozen graph into memory")
        graphDef = tf.GraphDef()

        with tf.gfile.GFile(args["model"], "rb") as f:
            serializedGraph = f.read()
            graphDef.ParseFromString(serializedGraph)
            tf.import_graph_def(graphDef, name="")
        print(">  ====== NAIL Inference graph loaded.")

    with model.as_default():
        with tf.Session(graph=model) as sess:
            imageTensor = model.get_tensor_by_name("image_tensor:0")
            boxesTensor = model.get_tensor_by_name("detection_boxes:0")

            scoresTensor = model.get_tensor_by_name("detection_scores:0")
            classesTensor = model.get_tensor_by_name("detection_classes:0")
            numDetections = model.get_tensor_by_name("num_detections:0")
            image = cv2.flip(image, 1)

            (H, W) = image.shape[:2]
            output = image.copy()
            rgba = cv2.cvtColor(output, cv2.COLOR_RGB2RGBA)

            img_ff, bin_mask, res = ff.find_hand_old(image.copy())
            image = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
            image = np.expand_dims(image, axis=0)

            (boxes, scores, labels, N) = sess.run(
                [boxesTensor, scoresTensor, classesTensor, numDetections],
                feed_dict={imageTensor: image})
            boxes = np.squeeze(boxes)
            scores = np.squeeze(scores)
            labels = np.squeeze(labels)
            # mask with transparent nails
            mask = np.full((H, W), 255, dtype=np.uint8)

            for (box, score, label) in zip(boxes, scores, labels):
                if score < args["min_confidence"]:
                    continue
                box_multiplier = 1.1
                (startY, startX, endY, endX) = box
                startX = int(startX * W / box_multiplier)
                startY = int(startY * H / box_multiplier)
                endX = int(endX * W * box_multiplier)
                endY = int(endY * H * box_multiplier)
                cv2.rectangle(mask, (startX, startY), (endX, endY), 0, -1)

            rgba[:, :, 3] = mask
            rgba = cv2.flip(rgba, 1)
            rgba = rgba[0:min(H, W), 0:min(H, W)]

            # Save the output image to a file
            output_filename = os.path.join(os.path.dirname(image_path), f"{uuid.uuid4()}.png")
            cv2.imwrite(output_filename, rgba)

            return output_filename
