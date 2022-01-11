# ============================================
#             HighSpeedCommand
# ============================================
class HighSpeedCommand(Command):
    """
    Runs the high speed demo.

    high_speed
        {paramFile : Yaml file with demo parameters.}
    """
    # -----
    # constructor
    # -----
    def __init__(self):
        super().__init__()

        self.signal = {"sine" : 1, "line" : 2}
        self.plot_data = {
            "requests" = [],
            "measurements" = [],
            "times" = [],
            "cycle_stop_times" = [],
            "dev_write_command_times" = [],
            "dev_read_command_times" = [],
        }

        matplotlib.use("WebAgg")
        if fxu.is_pi():
            matplotlib.rcParams.update({"webagg.address": "0.0.0.0"})

    # -----
    # handle
    # -----
    def handle(self):
        """
        Runs the high speed demo.
        """
        params = init(self.argument("paramFile"), self._validate)
        fxs = flex.FlexSEA()
        dt = 1.0 / (float(params["cmd_freq"]))
        samples = self._get_samples(params["signal_type"], params["signal_amplitude"], params["signal_freq"], params["cmd_freq"], params["request_jitter"], params["jitter"])

        for port in ports:
            input("Press 'ENTER' to continue...")
            self._reset_plot()
            device = Device(fxs, port, params["baud_rate"])
            device.set_controller(params["controller_type"])
            self._high_speed(device, params["nLoops"], samples, dt)
            device.motor(fxe.FX_NONE, 0)
            sleep(0.1)
            self._plot()
            device.close()

    # -----
    # _get_samples
    # -----
    def _get_samples(self, sig_type, amp, sig_freq, cmd_freq, request_jitter, jitter):
        """
        Generates sample values for the demo.

        Parameters
        ----------
        sig_type : int
            Either 1 for "sine" or  2 for "line".

        amp : int
            The max height of the signal.

        sig_freq : int
            Frequency of the sine wave. Only applies if `signal_type` is "sine".

        cmd_freq : int
            The sampling frequency.

        request_jitter : bool
            Flag indicating whether or not jitter should be added to the
            generated samples.

        jitter : int
            The amount of jitter to add to the samples, if desired.

        Returns
        -------
        np.ndarray
            An array containing the samples to use in the demo.
        """
        np.random.seed(42)
        if sig_type not in self.signal.values():
            raise ValueError(f"Unsupported signal type: `{sig_type}`")
        f = sig_freq if sig_type == self.signal["sine"] else 1
        samples = fxu.sin_generator(amp, f, cmd_freq)
        if request_jitter:
            samples = samples + np.random.normal(loc=jitter, size=samples.shape)
        print("Command table:")
        print(np.int64(samples))
        return samples

    # -----
    # _high_speed
    # -----
    def _high_speed(self, device, nLoops, samples, dt):
        start_time = time()
        if device.controller_type == fxe.HSS_POSITION:
            sleep(0.1)
            data = device.read()
            pos0 = data.mot_ang
        else:
            pos0 = 0

        for rep in range(nLoops):
            elapsed_time = time() - start_time
            fxu.print_loop_count_and_time(rep, nLoops, elapsed_time)

            for sample in samples:
                sleep(delay_time)
                if device.controller_type != fxe.HSS_CURRENT:
                    sample = sample + pos0

                # Read
                begin_time = time()
                data = device.read()
                self.plot_data["dev_read_command_times"].append(time() - begin_time)

                # Write
                begin_time = time()
                device.motor(device.controller, sample)
                self.plot_data["dev_write_command_times"].append(time() - begin_time)

                if device.controller == fxe.FX_CURRENT:
                    val = data.mot_cur
                else:
                    val = data.mot_ang - pos0

                self.plot_data["times"].append(time() - start_time)
                self.plot_data["measurements"].append(val)
                self.plot_data["requests"].append(sample)

            # Delay between cycles (sine wave only)
            if signal_type == self.signal["sine"]:
                for _ in range(int(cycle_delay / delay_time)):
                    sleep(delay_time)
                    data = fxs.read_device(dev_id)

                    if device.controller_type == fxe.HSS_CURRENT:
                        self.plot_data["measurements"].append(data.mot_cur)
                    elif device.controller_type == fxe.HSS_POSITION:
                        self.plot_data["measurements"].append(data.mot_ang - pos0)

                    plot_data["times"].append(time() - start_time)
                    plot_data["requests"].append(sample)

            # We'll draw a line at the end of every period
            self.plot_data["cycle_stop_times"].append(time() - start_time)

    # -----
    # _reset_plot
    # -----
    def _reset_plot(self):
        self.plot_data = {
            "requests" = [],
            "measurements" = [],
            "times" = [],
            "cycle_stop_times" = [],
            "dev_write_command_times" = [],
            "dev_read_command_times" = [],
        }
        plt.clf()

    # -----
    # _validate
    # -----
    def _validate(self, params):
        """
        The read_only demo requires at least one port, a baud rate,
        and a run time.

        Parameters
        ----------
        params : dict
            The demo parameters read from the parameter file.

        Raises
        ------
        KeyError
            If a required parameter isn't found.

        ValueError
            If the value given for a parameter is invalid.

        Returns
        -------
        params : dict
            The validated parameters.
        """
        win_max_freq = 100
        if fxu.is_win() and params["cmd_freq"] > win_max_freq:
            params["cmd_freq"] = win_max_freq
            print(f"Capping the command frequency in Windows to {win_max_freq}")
        return params
