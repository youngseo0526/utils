import os
import glob
import natsort
import numpy as np
import argparse

def _calc_distances(preds, targets, mask, normalize):
    """Calculate the normalized distances between preds and target.

    Note:
        batch_size: N
        num_keypoints: K
        dimension of keypoints: D (normally, D=2 or D=3)

    Args:
        preds (np.ndarray[N, K, D]): Predicted keypoint location.
        targets (np.ndarray[N, K, D]): Groundtruth keypoint location.
        mask (np.ndarray[N, K]): Visibility of the target. False for invisible
            joints, and True for visible. Invisible joints will be ignored for
            accuracy calculation.
        normalize (np.ndarray[N, D]): Typical value is heatmap_size

    Returns:
        np.ndarray[K, N]: The normalized distances. \
            If target keypoints are missing, the distance is -1.
    """
    N, K, _ = preds.shape
    # set mask=0 when normalize==0
    _mask = mask.copy().astype(bool)
    _mask[np.where((normalize == 0).sum(1))[0], :] = False
    distances = np.full((N, K), -1, dtype=np.float32)
    # handle invalid values
    normalize[np.where(normalize <= 0)] = 1e6
    distances[_mask] = np.linalg.norm(((preds - targets) / normalize[:, None, :])[_mask], axis=-1)
    return distances.T

def _distance_acc(distances, thr):
    """Return the percentage below the distance threshold, while ignoring
    distances values with -1.

    Note:
        batch_size: N
    Args:
        distances (np.ndarray[N, ]): The normalized distances.
        thr (float): Threshold of the distances.

    Returns:
        float: Percentage of distances below the threshold. \
            If all target keypoints are missing, return -1.
    """
    #import pdb; pdb.set_trace()
    distance_valid = distances != -1
    num_distance_valid = distance_valid.sum()
    if num_distance_valid > 0:
        return (distances[distance_valid] < thr).sum() / num_distance_valid
    return -1

def keypoint_pck_accuracy(pred, gt, mask, thr, normalize):
    """Calculate the pose accuracy of PCK for each individual keypoint and the
    averaged accuracy across all keypoints for coordinates.

    Note:
        PCK  measures accuracy of the localization of the body joints.
        The distances between predicted positions and the ground-truth ones
        are typically normalized by the bounding box size.
        The threshold (thr) of the normalized distance is commonly set
        as 0.05, 0.1 or 0.2 etc.

        - batch_size: N
        - num_keypoints: K

    Args:
        pred (np.ndarray[N, K, 2]): Predicted keypoint location.
        gt (np.ndarray[N, K, 2]): Groundtruth keypoint location.
        mask (np.ndarray[N, K]): Visibility of the target. False for invisible
            joints, and True for visible. Invisible joints will be ignored for
            accuracy calculation.
        thr (float): Threshold of PCK calculation.
        normalize (np.ndarray[N, 2]): Normalization factor for H&W.

    Returns:
        tuple: A tuple containing keypoint accuracy.

        - acc (np.ndarray[K]): Accuracy of each keypoint.
        - avg_acc (float): Averaged accuracy across all keypoints.
        - cnt (int): Number of valid keypoints.
    """
    distances = _calc_distances(pred, gt, mask, normalize)
    #import pdb; pdb.set_trace()
    acc = np.array([_distance_acc(d, thr) for d in distances])
    valid_acc = acc[acc >= 0]
    cnt = len(valid_acc)
    avg_acc = valid_acc.mean() if cnt > 0 else 0
    return avg_acc

def keypoint_nme(pred, gt, mask, normalize_factor):
    """Calculate the normalized mean error (NME).

    Note:
        - batch_size: N
        - num_keypoints: K

    Args:
        pred (np.ndarray[N, K, 2]): Predicted keypoint location.
        gt (np.ndarray[N, K, 2]): Groundtruth keypoint location.
        mask (np.ndarray[N, K]): Visibility of the target. False for invisible
            joints, and True for visible. Invisible joints will be ignored for
            accuracy calculation.
        normalize_factor (np.ndarray[N, 2]): Normalization factor.

    Returns:
        float: normalized mean error
    """
    import pdb; pdb.set_trace()
    distances = _calc_distances(pred, gt, mask, normalize_factor)
    distance_valid = distances[distances != -1]

    #nme_pupil
    ocular_dists = np.sqrt(np.sum((gt[:, 72] - gt[:, 60])**2, axis=1))
    norm_dists = np.sqrt(np.sum((gt - pred)**2, axis=2)) / ocular_dists.reshape(len(gt), 1)

    return distance_valid.sum() / max(1, len(distance_valid)), norm_dists * 100

def eval_(args):
    gt_list = natsort.natsorted(glob.glob(args.gt_root+f'/*.txt',recursive=True))
    pred_list = natsort.natsorted(glob.glob(args.pred_root+f'/*.txt',recursive=True))

    thr = args.thr
    normalize_factor = args.normalize_factor
    batch_size = args.batch_size

    i = 0
    if args.metric == 'pck':
        pck_true = num_valid_data = 0
        for gt, pred in zip(gt_list, pred_list):
            loaded_pred_data = np.loadtxt(pred_list[i], usecols=(0, 1))
            pred_keypoint = np.expand_dims(loaded_pred_data, axis=0)

            loaded_gt_data = np.loadtxt(gt_list[i], usecols=(0, 1))
            gt_keypoint = np.expand_dims(loaded_gt_data, axis=0)
            gt_mask = np.loadtxt(gt_list[i], usecols=(2))
            gt_mask = np.expand_dims(gt_mask, axis=0)
            
            normalize = np.full((batch_size, len(loaded_gt_data[0])), normalize_factor)
            
            if sum(gt_mask[0]) != 0.0:
                pck_ = keypoint_pck_accuracy(pred_keypoint, gt_keypoint, gt_mask, thr, normalize)
                pck_true += pck_
                num_valid_data += 1

            i += 1

        pck = (pck_true / num_valid_data) * 100
        print(f"Valid data: {num_valid_data}    True: {int(pck_true)}    False: {int((num_valid_data - pck_true))}    PCK@{thr}:", pck)
    
    if args.metric =='nme':
        nme_sum = num_valid_data = nme_pupil_sum = 0
        for gt, pred in zip(gt_list,pred_list):
            loaded_pred_data = np.loadtxt(pred_list[i], usecols=(0, 1))
            pred_keypoint = np.expand_dims(loaded_pred_data, axis=0)

            #import pdb; pdb.set_trace()
            loaded_gt_data = np.loadtxt(gt_list[i], usecols=(0, 1))
            gt_keypoint = np.expand_dims(loaded_gt_data, axis=0)
            gt_mask = np.loadtxt(gt_list[i], usecols=(2))
            gt_mask = np.expand_dims(gt_mask, axis=0)

            normalize = np.full((batch_size, len(loaded_gt_data[0])), normalize_factor)
            
            if sum(gt_mask[0]) != 0.0:
                nme_, nme_pupil_ = keypoint_nme(pred_keypoint, gt_keypoint, gt_mask, normalize)
                nme_sum += nme_
                nme_pupil_sum += nme_pupil_
                num_valid_data += 1
            i += 1

        nme = nme_sum / len(pred_list)
        nme_pupil = nme_sum / len(pred_list)
        print(f"Valid data: {num_valid_data}    NME: {nme},  NME_pupil: {nme_pupil}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--metric', choices=['nme', 'pck'], default='nme')
    parser.add_argument('--gt_root', type=str, default='/input/yskim/keypoint/experiments/a person_r3_10000/selected')
    parser.add_argument('--pred_root', type=str, default='/input/yskim/keypoint/experiments/a person_r3_10000/selected_aug')
    parser.add_argument('--thr', type=float, default=0.5)
    parser.add_argument('--normalize_factor', type=int, default=1)
    parser.add_argument('--batch_size', type=int, default=1)

    args = parser.parse_args()

    eval_(args)